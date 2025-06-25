# -*- coding: utf-8 -*-
from odoo import Command, models, _, release
from requests.auth import HTTPBasicAuth
from odoo.exceptions import ValidationError
from pypdf import PdfReader
from pdf2image import convert_from_bytes
from PIL import Image
from dateutil.parser import parse

import logging
import re
import io
import base64
import pytesseract
import traceback
import uuid
import requests
import numpy as np
import cv2

_logger = logging.getLogger(__name__)


class InvoiceDigitizerProcessor(models.AbstractModel):
    _name = 'invoice.digitizer.processor'

    def extract_invoice_data(self, attachment, invoice=False):
        try:
            invoice = invoice or self.env['account.move'].create({})
            user_prompt = self.user_prompt(attachment)
            file_data = attachment.datas
            file_name = attachment.name

            response_data = self._make_api_request(file_data, file_name)
            partner_id = self._partner_from_response(response_data)
            line_ids = self._invoice_lines_from_response(response_data, invoice.move_type)

            extracted_values = {
                'ref': response_data.get('InvoiceNumber'),
                'invoice_date': response_data.get('InvoiceDate') and parse(response_data.get('InvoiceDate')).date(),
                'invoice_date_due': response_data.get('DueDate') and parse(response_data.get('DueDate')).date(),
                'invoice_line_ids': line_ids,
                'narration': response_data.get('TermsAndConditions') or response_data.get('TermsandConditions'),
                'partner_id': partner_id and partner_id.id,
            }

            invoice.write(extracted_values)
            msg = _("Attachment %s scanned and parsed with AI.", attachment.name)
            invoice.message_post(body=msg)

            return invoice

        except Exception as e:
            _logger.error(f'{e}\n{traceback.format_exc()}')
            if invoice:
                msg = _(
                    "There was a problem with digitizing the attachment %s. Please try again or check server logs for more information.",
                    attachment.name)
                invoice.message_post(body=msg)
                raise ValidationError(msg)

            return invoice or self.env['account.move']

    def _partner_from_response(self, response_dict):
        partner_id = self.env['res.partner'].browse()
        name = (response_dict.get('BillTo') or response_dict.get('BuyerName') or response_dict.get('CustomerName')
                or response_dict.get('Customer') or response_dict.get('VendorName'))

        if name:
            domain = [('is_company', '=', True), ('id', '!=', self.env.company.id)]
            domain.append(('name', '=', name))
            partner_id = self.env['res.partner'].search(domain, limit=1)

        return partner_id

    def _invoice_lines_from_response(self, response_dict, move_type):
        line_ids = [Command.clear()]
        for line in response_dict.get('ItemDetails', []):
            def extract_number(value):
                if value:
                    cleaned_value = re.sub(r'[^\d.]+', '', value)
                    try:
                        return float(cleaned_value) if cleaned_value else 0.0
                    except ValueError:
                        return 0.0
                return 0.0

            quantity_str = line.get('Quantity', '')
            price_unit_str = line.get('UnitPrice', '')
            discount_str = line.get('Discount', '') or line.get('Disc.%', '')
            vat_rate_str = line.get('Taxes', '') or line.get('Tax', '')

            quantity = extract_number(quantity_str)
            price_unit = extract_number(price_unit_str)
            discount = extract_number(discount_str)
            vat_rate = extract_number(vat_rate_str)

            vat_rates = [extract_number(vat) for vat in vat_rate_str.split(',')]

            if move_type in ('in_invoice', 'in_refund'):
                type_tax_use = 'purchase'
            else:
                type_tax_use = 'sale'

            tax_ids = []
            for vat_rate in vat_rates:
                if vat_rate:
                    tax_id = self.env['account.tax'].search([
                        ('type_tax_use', '=', type_tax_use),
                        ('amount', '=', vat_rate),
                        ('amount', '!=', 0.0),
                        ('active', '=', True)
                    ])
                    tax_ids.extend(tax_id.ids)

            line_ids.append(
                Command.create({
                    'name': line.get('Description'),
                    'quantity': quantity,
                    'price_unit': price_unit,
                    'discount': discount,
                    'tax_ids': tax_ids
                })
            )

        return line_ids

    def _make_api_request(self, file_data, file_name):

        try:
            api_endpoint = 'https://us-central1-serene-essence-419307.cloudfunctions.net/odooinvoice'

            payload = {
                'jsonrpc': '2.0',
                'method': 'call',
                'params': {
                    'version': release.version,
                },
                'id': uuid.uuid4().hex,
            }

            file_content = base64.b64decode(file_data)

            files = {
                'invoice': (file_name, file_content, 'application/pdf')
            }
            username = self.env.company.inv_username
            password = self.env.company.inv_password
            if not username:
                username = False
            if not password:
                password = False

            response = requests.post(
                api_endpoint,
                files=files,
                auth=HTTPBasicAuth(username, password),
                json=payload,
                timeout=30,
            )
            response.raise_for_status()



            response_data = response.json()

            if 'error' in response_data:
                message = response_data['error']['data'].get('message')
                raise ValidationError(message)
            return response_data

        except Exception as error:
            raise ValidationError(_(error))

    def user_prompt(self, attachment):
        text = self._process_attachments_for_text_extraction(attachment)
        return text

    def _process_attachments_for_text_extraction(self, attachments):
        attachment_data = ''
        for i, attachment in enumerate(attachments, start=1):
            content = base64.b64decode(attachment.with_context(bin_size=False).datas)
            f = io.BytesIO(content)

            if 'pdf' in attachment.mimetype:
                parsed_data = self._parse_pdf_for_data(f)
                if parsed_data == '':
                    images = convert_from_bytes(content)
                    for image in images:
                        parsed_data += self._parse_image_for_data(image)
                attachment_data += f'File {i}: --- {parsed_data} --- '
            elif 'image' in attachment.mimetype:
                attachment_data += f'File {i}: --- {self._parse_image_for_data(f)} --- '

        return attachment_data.strip()

    @staticmethod
    def _parse_pdf_for_data(f):
        parsed_data = ''
        reader = PdfReader(f)
        for page in reader.pages:
            parsed_data += page.extract_text()
        return parsed_data

    def _parse_image_for_data(self, f):
        try:
            img = Image.open(f)
        except AttributeError:
            img = f
        img = self._preprocess_image(img)
        langs = '+'.join(pytesseract.get_languages())
        text = pytesseract.image_to_string(img, lang=langs)
        return text

    @staticmethod
    def _preprocess_image(image):
        image_array = np.asarray(image)
        channels = image_array.shape[-1] if image_array.ndim == 3 else 1
        if channels == 3:
            image = cv2.resize(image_array, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            kernel = np.ones((5, 5), np.uint8)
            image = cv2.erode(image, kernel, iterations=1)
        return image

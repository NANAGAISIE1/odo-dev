import base64
import re
import urllib.parse  # Ensure this import is present

from odoo import _, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_whatsapp_share_url(self):
        self.ensure_one()
        if not self.partner_id:
            raise UserError(_("Customer (partner) is not set on this invoice."))

        phone_number = self.partner_id.phone or self.partner_id.mobile
        if not phone_number:
            raise UserError(
                _("The customer does not have a phone or mobile number configured.")
            )

        cleaned_phone = re.sub(r"[^\d+]", "", phone_number)
        final_phone = ""  # Initialize final_phone

        if (
            not cleaned_phone.startswith("+")
            and self.partner_id.country_id
            and self.partner_id.country_id.phone_code
        ):
            country_code = str(self.partner_id.country_id.phone_code)
            if cleaned_phone.startswith("0"):
                cleaned_phone = cleaned_phone[1:]
            final_phone = country_code + cleaned_phone
        elif cleaned_phone.startswith("+"):
            final_phone = cleaned_phone
        else:
            final_phone = cleaned_phone

        if not final_phone:  # Should be caught by earlier checks, but as a safeguard
            raise UserError(
                _("Could not determine a valid phone number for the customer.")
            )

        # PDF Generation and Attachment
        report_action_name = "account.account_invoices"  # Standard Odoo invoice report
        report_action = self.env.ref(report_action_name, raise_if_not_found=False)

        if not report_action:
            # _logger.error(f"Report action '{report_action_name}' not found.") # Optional logging
            raise UserError(
                _(
                    "The invoice report action '%s' could not be found. Please check your Odoo setup."
                )
                % report_action_name
            )

        # Check if report_action.report_name is a string, as it's used internally by Odoo
        if not isinstance(report_action.report_name, str):
            # _logger.error(f"Report action '{report_action_name}' (ID: {report_action.id}) has an invalid report_name type: {type(report_action.report_name)}. Value: {report_action.report_name}")
            raise UserError(
                _(
                    "The configuration for report action '%s' is invalid. Its 'report_name' attribute is not a string, which can cause errors during PDF generation. Please contact an administrator."
                )
                % report_action_name
            )

        pdf_content = None
        try:
            pdf_content, content_type = report_action._render_qweb_pdf(self.ids)
        except AttributeError as e_render:
            if (
                "split" in str(e_render).lower() and "list" in str(e_render).lower()
            ):  # Check if the error message indicates a list.split() issue
                # _logger.error(f"AttributeError (likely list.split) during PDF generation for report '{report_action.report_name}' and invoice {self.name} (ID: {self.id}): {e_render}", exc_info=True) # Optional logging
                raise UserError(
                    _(
                        "Failed to generate PDF due to a configuration issue. It seems a setting that should be text is incorrectly a list. Details: %s"
                    )
                    % str(e_render)
                )
            # _logger.error(f"Unexpected AttributeError during PDF generation for invoice {self.name} (ID: {self.id}): {e_render}", exc_info=True) # Optional logging
            raise UserError(
                _("An error occurred while generating the PDF: %s") % str(e_render)
            )
        except Exception as e_render_generic:
            # _logger.error(f"Generic error during PDF generation for invoice {self.name} (ID: {self.id}): {e_render_generic}", exc_info=True) # Optional logging
            raise UserError(
                _(
                    "An unexpected error occurred while generating the PDF for the invoice: %s"
                )
                % str(e_render_generic)
            )

        if not pdf_content:
            raise UserError(_("Failed to generate PDF content for the invoice."))

        attachment_name = (
            f"{self.name.replace('/', '_') if self.name else 'invoice'}_whatsapp.pdf"
        )

        existing_attachment = self.env["ir.attachment"].search(
            [
                ("name", "=", attachment_name),
                ("res_model", "=", "account.move"),
                ("res_id", "=", self.id),
            ],
            limit=1,
        )

        if existing_attachment:
            attachment = existing_attachment
            # Optionally, update existing attachment if content might change:
            # existing_attachment.write({'datas': base64.b64encode(pdf_content)})
        else:
            attachment_vals = {
                "name": attachment_name,
                "datas": base64.b64encode(pdf_content),
                "res_model": "account.move",
                "res_id": self.id,
                "type": "binary",
                "mimetype": "application/pdf",
            }
            attachment = self.env["ir.attachment"].create(attachment_vals)

        if not attachment or not attachment.id:
            raise UserError(
                _("Could not create or find PDF attachment for the invoice.")
            )

        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        if not base_url:
            raise UserError(
                _(
                    "The web base URL is not configured in Odoo. Please set 'web.base.url' in system parameters."
                )
            )

        # attachment.name should be URL-safe, but quoting is safer
        safe_attachment_name = urllib.parse.quote(attachment.name or "invoice.pdf")
        download_url = f"{base_url}/web/content/{attachment.id}/{safe_attachment_name}?download=true&access_token={attachment.access_token}"

        partner_name = self.partner_id.name or "Customer"
        message_parts = [
            _("Dear %s,") % partner_name,
            _("Please find your invoice %s (Amount: %s %s).")
            % (self.name or _("N/A"), self.amount_total, self.currency_id.symbol or ""),
            _("You can download the PDF here: %s") % download_url,
            _(
                "Kindly attach the downloaded PDF to this message if it's not already attached by your system."
            ),
        ]
        message = "\n\n".join(m for m in message_parts if m)  # Join non-empty parts

        encoded_message = urllib.parse.quote(message)
        whatsapp_url = (
            f"https://web.whatsapp.com/send?phone={final_phone}&text={encoded_message}"
        )

        return whatsapp_url

    def action_whatsapp_share(self):
        self.ensure_one()
        if self.move_type not in ("out_invoice", "out_refund"):
            raise UserError(
                _(
                    "WhatsApp sharing is only available for customer invoices and refunds."
                )
            )

        try:
            whatsapp_url = self._get_whatsapp_share_url()
            return {
                "type": "ir.actions.act_url",
                "url": whatsapp_url,
                "target": "new",
            }
        except UserError:  # Catch UserErrors raised by _get_whatsapp_share_url
            raise
        except Exception as e:
            # _logger.error("Error in action_whatsapp_share for invoice %s: %s", self.name, str(e), exc_info=True) # Optional logging
            # Provide a more generic error for unexpected issues, but the specific one should be caught above
            raise UserError(
                _(
                    "An unexpected error occurred while preparing the WhatsApp message: %s"
                )
                % str(e)
            )

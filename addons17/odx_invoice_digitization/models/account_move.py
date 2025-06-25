# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    enable_invoice_digitizer = fields.Boolean(compute='_compute_enable_invoice_digitizer')

    @api.depends('move_type')
    def _compute_enable_invoice_digitizer(self):
        accepted_types = ['in_invoice', 'out_invoice', 'out_refund', 'in_refund']
        for record in self:
            record.enable_invoice_digitizer = record.move_type in accepted_types and record.state == 'draft'

    def action_digitize_invoice(self):
        attachments = self.env['ir.attachment'].search([('res_model', '=', 'account.move'), ('res_id', '=', self.id)])
        for attachment in attachments:
            self.env['invoice.digitizer.processor'].extract_invoice_data(attachment, self)

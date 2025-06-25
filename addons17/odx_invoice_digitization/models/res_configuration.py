# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    inv_username = fields.Char('Invoice Digitization Username', related='company_id.inv_username', readonly=False)
    inv_password = fields.Char('Invoice Digitization Password', related='company_id.inv_password', readonly=False)

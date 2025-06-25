# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    inv_username = fields.Char('Invoice Digitization Username')
    inv_password = fields.Char('Invoice Digitization Password')

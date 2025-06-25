from odoo import fields, models


class BusinessPreference(models.Model):
    _name = "business_core.business_preference"
    _description = "Business Preference"

    link_id = fields.Char(string="Link ID", size=100)
    sources = fields.Text(string="Sources")
    type = fields.Char(string="Type", size=20)

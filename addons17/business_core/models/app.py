from odoo import fields, models


class App(models.Model):
    _name = "business_core.app"
    _description = "Business App"

    name = fields.Char(string="Name", size=50, required=True)
    summary = fields.Text(string="Summary")
    image = fields.Char(string="Image URL", size=200)
    link = fields.Char(string="App Link", size=300)
    cost = fields.Integer(string="Cost")

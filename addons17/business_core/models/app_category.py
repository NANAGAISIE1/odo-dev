from odoo import fields, models


class AppCategory(models.Model):
    _name = "business_core.app_category"
    _description = "Application Category"

    name = fields.Char(string="Name", size=50, required=True)
    summary = fields.Text(string="Summary")
    color = fields.Char(string="Color", size=50)
    image = fields.Char(string="Image URL", size=100)
    apps = fields.Many2many(
        "business_core.app",
        string="Apps",
        help="List of applications in this category",
    )
    parent = fields.Many2one(
        "business_core.app_category",
        string="Parent Category",
        help="Parent category for hierarchical categorization",
    )
    date_added = fields.Char(string="Date Added", size=20)

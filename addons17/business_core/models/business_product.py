from odoo import fields, models


class BusinessProduct(models.Model):
    _name = "business_core.business_product"
    _description = "Business Product"

    name = fields.Char(string="Product Name", size=50, required=True)
    instances = fields.Integer(string="Instances")
    features = fields.Text(string="Features")
    date_added = fields.Char(string="Date Added", size=20)
    last_update = fields.Char(string="Last Update", size=20)
    category = fields.Char(string="Category", size=50)
    status = fields.Char(string="Status", size=20)
    subscription_id = fields.Char(string="Subscription ID", size=20)
    product_id = fields.Char(string="Product ID", size=20)
    business_id = fields.Many2one("business_core.business", string="Business")

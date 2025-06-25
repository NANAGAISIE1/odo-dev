from odoo import fields, models


class Business(models.Model):
    _name = "business_core.business"
    _description = "Business"
    _rec_name = "name"

    uid = fields.Char(string="UID", size=100)
    business_type = fields.Char(string="Business Type", size=50)
    email = fields.Char(string="Email", size=50)
    name = fields.Char(string="Name", size=50)
    abbrev = fields.Char(string="Abbreviation", size=50)
    country = fields.Char(string="Country", size=50)
    address = fields.Char(string="Address", size=100)
    phone = fields.Char(string="Phone", size=50)
    industry = fields.Char(string="Industry", size=50)
    is_verified = fields.Boolean(string="Verified", default=False)
    business_license = fields.Char(string="Business License", size=100)
    business_idnumber = fields.Char(string="Business ID Number", size=50)
    business_idtype = fields.Char(string="Business ID Type", size=50)
    subscription_id = fields.Char(string="Subscription ID", size=50)
    logo = fields.Char(string="Logo URL", size=200)
    summary = fields.Text(string="Summary")

from odoo import fields, models


class Kyc(models.Model):
    _name = "identity_core.kyc"
    _description = "KYC Verification Record"
    _order = "date_added desc"

    uid = fields.Char(string="User UID", required=True)
    kyc_uuid = fields.Char(string="KYC UUID", required=True, copy=False, readonly=True)
    status = fields.Selection(
        [("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")],
        string="Status",
        default="pending",
    )
    info = fields.Text(string="KYC Info")
    org_id = fields.Char(string="Organization ID")
    org_name = fields.Char(string="Organization Name")
    date_added = fields.Datetime(
        string="Date Added", default=fields.Datetime.now, readonly=True
    )
    date_updated = fields.Datetime(
        string="Date Updated", default=fields.Datetime.now, readonly=True
    )

from odoo import fields, models


class AuthOAuthProvider(models.Model):
    _inherit = "auth.oauth.provider"

    x_keycloak = fields.Boolean(
        string="Keycloak",
        default=False,
        help="Check this box if this OAuth provider is a Keycloak provider.",
        store=True,
    )

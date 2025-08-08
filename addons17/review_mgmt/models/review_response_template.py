# -*- coding: utf-8 -*-
from odoo import fields, models


class ReviewResponseTemplate(models.Model):
    _name = "review.response.template"
    _description = "Response Template"

    name = fields.Char(required=True)
    body = fields.Html(required=True)
    active = fields.Boolean(default=True)

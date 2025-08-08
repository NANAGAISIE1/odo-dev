# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class ReviewListing(models.Model):
    _name = "review.listing"
    _description = "Review Listing (Product/Service/Location)"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name, id"

    name = fields.Char(required=True, tracking=True)
    active = fields.Boolean(default=True)
    listing_type = fields.Selection(
        [("product", "Product"), ("service", "Service"), ("other", "Other")],
        required=True,
        default="product",
        tracking=True,
    )
    external_ref = fields.Char(help="External platform reference (SKU, page id, etc.)")
    platform = fields.Selection(
        [
            ("manual", "Manual"),
            ("shopify", "Shopify"),
            ("woocommerce", "WooCommerce"),
            ("google", "Google"),
            ("facebook", "Facebook"),
            ("x", "X / Twitter"),
            ("other", "Other"),
        ],
        default="manual",
        required=True,
        tracking=True,
    )

    review_ids = fields.One2many("review.review", "listing_id", string="Reviews")
    review_count = fields.Integer(compute="_compute_counts", store=True)
    avg_rating = fields.Float(compute="_compute_avg_rating", store=True, digits=(16, 2))

    @api.depends("review_ids.rating")
    def _compute_avg_rating(self):
        for rec in self:
            ratings = rec.review_ids.mapped("rating")
            rec.avg_rating = sum(ratings) / len(ratings) if ratings else 0.0

    @api.depends("review_ids")
    def _compute_counts(self):
        for rec in self:
            rec.review_count = len(rec.review_ids)

    def action_view_reviews(self):
        self.ensure_one()
        action = self.env.ref("review_mgmt.action_review_review").read()[0]
        action["domain"] = [("listing_id", "=", self.id)]
        action["context"] = {"default_listing_id": self.id}
        return action

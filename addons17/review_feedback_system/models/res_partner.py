from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # Review fields
    review_ids = fields.One2many(
        "review.feedback",
        "partner_id",
        string="Reviews",
        help="Reviews submitted by this customer",
    )

    review_count = fields.Integer(
        string="Review Count",
        compute="_compute_review_count",
        help="Total number of reviews submitted",
    )

    average_rating_given = fields.Float(
        string="Average Rating Given",
        compute="_compute_average_rating_given",
        help="Average rating this customer gives in reviews",
    )

    def _compute_review_count(self):
        """Compute the number of reviews for each partner."""
        for partner in self:
            partner.review_count = len(partner.review_ids)

    def _compute_average_rating_given(self):
        """Compute average rating given by customer."""
        for partner in self:
            approved_reviews = partner.review_ids.filtered(
                lambda r: r.state == "approved" and r.rating
            )
            if approved_reviews:
                total_rating = sum(float(review.rating) for review in approved_reviews)
                partner.average_rating_given = total_rating / len(approved_reviews)
            else:
                partner.average_rating_given = 0.0

    def action_view_reviews(self):
        """Action to view customer reviews."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": f"Reviews by {self.name}",
            "res_model": "review.feedback",
            "view_mode": "tree,form",
            "domain": [("partner_id", "=", self.id)],
            "context": {"default_partner_id": self.id},
        }

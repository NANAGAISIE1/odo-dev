from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Review fields
    review_ids = fields.One2many(
        "review.feedback",
        "product_id",
        string="Reviews",
        domain=[("state", "=", "approved"), ("website_published", "=", True)],
        help="Customer reviews for this product",
    )

    review_count = fields.Integer(
        string="Review Count",
        compute="_compute_review_stats",
        store=True,
        help="Total number of approved reviews",
    )

    average_rating = fields.Float(
        string="Average Rating",
        compute="_compute_review_stats",
        store=True,
        help="Average rating from all approved reviews",
    )

    rating_distribution = fields.Text(
        string="Rating Distribution",
        compute="_compute_review_stats",
        store=True,
        help="JSON string containing rating distribution",
    )

    recommendation_rate = fields.Float(
        string="Recommendation Rate",
        compute="_compute_review_stats",
        store=True,
        help="Percentage of customers who would recommend this product",
    )

    @api.depends(
        "review_ids.rating",
        "review_ids.state",
        "review_ids.website_published",
        "review_ids.recommend",
    )
    def _compute_review_stats(self):
        """Compute review statistics for products."""
        import json

        for product in self:
            approved_reviews = product.review_ids.filtered(
                lambda r: r.state == "approved" and r.website_published
            )

            product.review_count = len(approved_reviews)

            if approved_reviews:
                # Calculate average rating
                total_rating = sum(float(review.rating) for review in approved_reviews)
                product.average_rating = total_rating / len(approved_reviews)

                # Calculate rating distribution
                distribution = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
                for review in approved_reviews:
                    distribution[review.rating] += 1
                product.rating_distribution = json.dumps(distribution)

                # Calculate recommendation rate
                recommended_count = len(approved_reviews.filtered("recommend"))
                product.recommendation_rate = (
                    recommended_count / len(approved_reviews)
                ) * 100
            else:
                product.average_rating = 0.0
                product.rating_distribution = json.dumps(
                    {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
                )
                product.recommendation_rate = 0.0

    def action_view_reviews(self):
        """Action to view product reviews."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": f"Reviews for {self.name}",
            "res_model": "review.feedback",
            "view_mode": "tree,form",
            "domain": [("product_id", "=", self.id)],
            "context": {"default_product_id": self.id},
        }

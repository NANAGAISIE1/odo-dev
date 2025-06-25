from odoo import _, api, fields, models


class ReviewCategory(models.Model):
    _name = "review.category"
    _description = "Review Category"
    _order = "sequence, name"

    name = fields.Char(
        string="Category Name",
        required=True,
        translate=True,
        help="Name of the review category",
    )

    description = fields.Text(
        string="Description",
        translate=True,
        help="Description of what this category covers",
    )

    sequence = fields.Integer(string="Sequence", default=10, help="Order of display")

    active = fields.Boolean(
        string="Active", default=True, help="Whether this category is active"
    )

    color = fields.Integer(string="Color", help="Color for category display")

    icon = fields.Char(string="Icon", help="FontAwesome icon class for this category")

    # Statistics
    review_count = fields.Integer(
        string="Review Count",
        compute="_compute_review_stats",
        store=True,
        help="Total number of reviews in this category",
    )

    average_rating = fields.Float(
        string="Average Rating",
        compute="_compute_review_stats",
        store=True,
        help="Average rating for reviews in this category",
    )

    # Website settings
    website_published = fields.Boolean(
        string="Published on Website",
        default=True,
        help="Whether this category is visible on website",
    )

    website_sequence = fields.Integer(
        string="Website Sequence", default=10, help="Order on website"
    )

    @api.depends("review_ids.rating", "review_ids.state")
    def _compute_review_stats(self):
        """Compute review statistics for each category."""
        for category in self:
            approved_reviews = category.review_ids.filtered(
                lambda r: r.state == "approved" and r.website_published
            )
            category.review_count = len(approved_reviews)

            if approved_reviews:
                total_rating = sum(float(review.rating) for review in approved_reviews)
                category.average_rating = total_rating / len(approved_reviews)
            else:
                category.average_rating = 0.0

    # Inverse relationship
    review_ids = fields.One2many(
        "review.feedback",
        "category_id",
        string="Reviews",
        help="Reviews in this category",
    )

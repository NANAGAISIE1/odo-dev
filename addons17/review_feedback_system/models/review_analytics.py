from odoo import fields, models, tools


class ReviewAnalytics(models.Model):
    _name = "review.analytics"
    _description = "Review Analytics"
    _auto = False
    _rec_name = "id"

    # Dimensions
    review_id = fields.Many2one("review.feedback", string="Review")
    partner_id = fields.Many2one("res.partner", string="Customer")
    product_id = fields.Many2one("product.template", string="Product")
    category_id = fields.Many2one("review.category", string="Category")

    # Time dimensions
    date = fields.Date(string="Date")
    month = fields.Char(string="Month")
    year = fields.Char(string="Year")
    quarter = fields.Char(string="Quarter")

    # Measures
    rating = fields.Float(string="Rating")
    rating_value = fields.Float(string="Rating Value")

    # States
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
            ("archived", "Archived"),
        ],
        string="Status",
    )

    website_published = fields.Boolean(string="Published on Website")
    verified_purchase = fields.Boolean(string="Verified Purchase")
    recommend = fields.Boolean(string="Would Recommend")

    # Counts
    review_count = fields.Integer(string="Review Count")
    helpful_count = fields.Integer(string="Helpful Count")

    def init(self):
        """Initialize the view."""
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """
            CREATE VIEW %s AS (
                SELECT
                    rf.id AS id,
                    rf.id AS review_id,
                    rf.partner_id,
                    rf.product_id,
                    rf.category_id,
                    rf.create_date::date AS date,
                    TO_CHAR(rf.create_date, 'YYYY-MM') AS month,
                    TO_CHAR(rf.create_date, 'YYYY') AS year,
                    TO_CHAR(rf.create_date, 'YYYY-Q') AS quarter,
                    CAST(rf.rating AS FLOAT) AS rating,
                    rf.rating_value,
                    rf.state,
                    rf.website_published,
                    rf.verified_purchase,
                    rf.recommend,
                    1 AS review_count,
                    rf.helpfulness_count AS helpful_count
                FROM review_feedback rf
                WHERE rf.state IN ('approved', 'submitted', 'rejected')
            )
        """
            % self._table
        )

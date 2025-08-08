from odoo import fields, models, tools


class ReviewAnalytics(models.Model):
    _name = "review.analytics"
    _description = "Review Analytics"
    _auto = False

    # Dimensions
    product_id = fields.Many2one("product.template", string="Product")
    category_id = fields.Many2one("review.category", string="Category")

    # Aggregated measures
    total_reviews = fields.Integer(string="Total Reviews")
    average_rating = fields.Float(string="Average Rating")
    five_star_count = fields.Integer(string="5★ Reviews")
    four_star_count = fields.Integer(string="4★ Reviews")
    three_star_count = fields.Integer(string="3★ Reviews")
    two_star_count = fields.Integer(string="2★ Reviews")
    one_star_count = fields.Integer(string="1★ Reviews")
    published_reviews = fields.Integer(string="Published Reviews")
    verified_reviews = fields.Integer(string="Verified Reviews")
    total_helpfulness_votes = fields.Integer(string="Total Helpfulness Votes")

    def init(self):
        """Create or replace the analytics SQL view (aggregated by product/category)."""
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            f"""
            CREATE VIEW {self._table} AS (
                SELECT
                    (COALESCE(rf.product_id, 0) * 1000000 + COALESCE(rf.category_id, 0))::BIGINT AS id,
                    rf.product_id,
                    rf.category_id,
                    COUNT(*) AS total_reviews,
                    AVG(CAST(rf.rating AS FLOAT)) AS average_rating,
                    COUNT(*) FILTER (WHERE rf.rating = '5') AS five_star_count,
                    COUNT(*) FILTER (WHERE rf.rating = '4') AS four_star_count,
                    COUNT(*) FILTER (WHERE rf.rating = '3') AS three_star_count,
                    COUNT(*) FILTER (WHERE rf.rating = '2') AS two_star_count,
                    COUNT(*) FILTER (WHERE rf.rating = '1') AS one_star_count,
                    COUNT(*) FILTER (WHERE rf.website_published) AS published_reviews,
                    COUNT(*) FILTER (WHERE rf.verified_purchase) AS verified_reviews,
                    COALESCE(SUM(rf.helpfulness_count), 0) AS total_helpfulness_votes
                FROM review_feedback rf
                WHERE rf.state IN ('approved', 'submitted', 'rejected')
                GROUP BY rf.product_id, rf.category_id
            )
            """
        )

    def update_analytics(self):
        """Public method to refresh the SQL view."""
        self.init()
        return True

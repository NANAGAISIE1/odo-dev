from odoo import api, fields, models


class ReviewSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # Review Moderation Settings
    auto_approve_verified_purchases = fields.Boolean(
        string="Auto-approve Verified Purchases",
        config_parameter="review_feedback_system.auto_approve_verified",
        help="Automatically approve reviews from verified purchases",
    )

    require_moderation = fields.Boolean(
        string="Require Moderation",
        default=True,
        config_parameter="review_feedback_system.require_moderation",
        help="All reviews require moderation before publishing",
    )

    allow_anonymous_reviews = fields.Boolean(
        string="Allow Anonymous Reviews",
        default=True,
        config_parameter="review_feedback_system.allow_anonymous",
        help="Allow users to submit reviews without registration",
    )

    min_rating_to_publish = fields.Selection(
        [
            ("1", "1 Star and above"),
            ("2", "2 Stars and above"),
            ("3", "3 Stars and above"),
            ("4", "4 Stars and above"),
            ("5", "5 Stars only"),
        ],
        string="Minimum Rating to Publish",
        default="1",
        config_parameter="review_feedback_system.min_rating_publish",
        help="Minimum rating required to publish reviews automatically",
    )

    # Email Notification Settings
    notify_on_new_review = fields.Boolean(
        string="Notify on New Reviews",
        default=True,
        config_parameter="review_feedback_system.notify_new_review",
        help="Send email notifications when new reviews are submitted",
    )

    notification_email = fields.Char(
        string="Notification Email",
        config_parameter="review_feedback_system.notification_email",
        help="Email address to receive review notifications",
    )

    # Website Display Settings
    reviews_per_page = fields.Integer(
        string="Reviews per Page",
        default=10,
        config_parameter="review_feedback_system.reviews_per_page",
        help="Number of reviews to display per page on website",
    )

    show_reviewer_name = fields.Boolean(
        string="Show Reviewer Name",
        default=True,
        config_parameter="review_feedback_system.show_reviewer_name",
        help="Display reviewer names on website",
    )

    allow_review_voting = fields.Boolean(
        string="Allow Review Voting",
        default=True,
        config_parameter="review_feedback_system.allow_voting",
        help="Allow visitors to vote on review helpfulness",
    )

    # Advanced Settings
    review_expiry_days = fields.Integer(
        string="Review Expiry (Days)",
        default=0,
        config_parameter="review_feedback_system.review_expiry_days",
        help="Days after which reviews are considered expired (0 = never)",
    )

    max_reviews_per_product_per_user = fields.Integer(
        string="Max Reviews per Product per User",
        default=1,
        config_parameter="review_feedback_system.max_reviews_per_product",
        help="Maximum number of reviews a user can submit per product",
    )

    @api.model
    def get_values(self):
        """Override to get configuration values."""
        res = super().get_values()
        params = self.env["ir.config_parameter"].sudo()

        res.update(
            {
                "auto_approve_verified_purchases": params.get_param(
                    "review_feedback_system.auto_approve_verified", False
                ),
                "require_moderation": params.get_param(
                    "review_feedback_system.require_moderation", True
                ),
                "allow_anonymous_reviews": params.get_param(
                    "review_feedback_system.allow_anonymous", True
                ),
                "min_rating_to_publish": params.get_param(
                    "review_feedback_system.min_rating_publish", "1"
                ),
                "notify_on_new_review": params.get_param(
                    "review_feedback_system.notify_new_review", True
                ),
                "notification_email": params.get_param(
                    "review_feedback_system.notification_email", ""
                ),
                "reviews_per_page": int(
                    params.get_param("review_feedback_system.reviews_per_page", 10)
                ),
                "show_reviewer_name": params.get_param(
                    "review_feedback_system.show_reviewer_name", True
                ),
                "allow_review_voting": params.get_param(
                    "review_feedback_system.allow_voting", True
                ),
                "review_expiry_days": int(
                    params.get_param("review_feedback_system.review_expiry_days", 0)
                ),
                "max_reviews_per_product_per_user": int(
                    params.get_param(
                        "review_feedback_system.max_reviews_per_product", 1
                    )
                ),
            }
        )
        return res

    def set_values(self):
        """Override to set configuration values."""
        super().set_values()
        params = self.env["ir.config_parameter"].sudo()

        params.set_param(
            "review_feedback_system.auto_approve_verified",
            self.auto_approve_verified_purchases,
        )
        params.set_param(
            "review_feedback_system.require_moderation", self.require_moderation
        )
        params.set_param(
            "review_feedback_system.allow_anonymous", self.allow_anonymous_reviews
        )
        params.set_param(
            "review_feedback_system.min_rating_publish", self.min_rating_to_publish
        )
        params.set_param(
            "review_feedback_system.notify_new_review", self.notify_on_new_review
        )
        params.set_param(
            "review_feedback_system.notification_email", self.notification_email or ""
        )
        params.set_param(
            "review_feedback_system.reviews_per_page", self.reviews_per_page
        )
        params.set_param(
            "review_feedback_system.show_reviewer_name", self.show_reviewer_name
        )
        params.set_param(
            "review_feedback_system.allow_voting", self.allow_review_voting
        )
        params.set_param(
            "review_feedback_system.review_expiry_days", self.review_expiry_days
        )
        params.set_param(
            "review_feedback_system.max_reviews_per_product",
            self.max_reviews_per_product_per_user,
        )

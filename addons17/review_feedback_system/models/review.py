import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Review(models.Model):
    _name = "review.feedback"
    _description = "Customer Review and Feedback"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"
    _rec_name = "title"

    # Basic Information
    title = fields.Char(
        string="Review Title",
        required=True,
        tracking=True,
        help="Short title for the review",
    )

    content = fields.Text(
        string="Review Content",
        required=True,
        tracking=True,
        help="Detailed review content",
    )

    rating = fields.Selection(
        [
            ("1", "1 Star - Poor"),
            ("2", "2 Stars - Fair"),
            ("3", "3 Stars - Good"),
            ("4", "4 Stars - Very Good"),
            ("5", "5 Stars - Excellent"),
        ],
        string="Rating",
        required=True,
        tracking=True,
    )

    rating_value = fields.Float(
        string="Rating Value",
        compute="_compute_rating_value",
        store=True,
        help="Numeric value of rating for calculations",
    )

    # Review Status
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
            ("archived", "Archived"),
        ],
        string="Status",
        default="draft",
        tracking=True,
    )

    # Customer Information
    partner_id = fields.Many2one(
        "res.partner", string="Customer", help="Customer who submitted the review"
    )

    customer_name = fields.Char(
        string="Customer Name", help="Name of the reviewer (for anonymous reviews)"
    )

    customer_email = fields.Char(string="Customer Email", help="Email of the reviewer")

    is_anonymous = fields.Boolean(
        string="Anonymous Review",
        default=False,
        help="Whether this is an anonymous review",
    )

    # Product/Service Information
    product_id = fields.Many2one(
        "product.template",
        string="Product/Service",
        help="Product or service being reviewed",
    )

    category_id = fields.Many2one(
        "review.category", string="Review Category", help="Category of the review"
    )

    # Additional Information
    pros = fields.Text(string="Pros", help="Positive aspects mentioned in review")
    cons = fields.Text(string="Cons", help="Negative aspects mentioned in review")

    recommend = fields.Boolean(
        string="Would Recommend",
        help="Whether the customer would recommend this product/service",
    )

    verified_purchase = fields.Boolean(
        string="Verified Purchase",
        default=False,
        help="Whether this review is from a verified purchase",
    )

    # Media Attachments
    attachment_ids = fields.Many2many(
        "ir.attachment",
        string="Attachments",
        help="Images or files attached to the review",
    )

    # Website Integration
    website_published = fields.Boolean(
        string="Published on Website",
        default=False,
        tracking=True,
        help="Whether this review is visible on the website",
    )

    website_url = fields.Char(
        string="Website URL",
        compute="_compute_website_url",
        help="URL where this review can be viewed on the website",
    )

    # Analytics Fields
    helpfulness_count = fields.Integer(
        string="Helpful Votes",
        default=0,
        help="Number of people who found this review helpful",
    )

    total_votes = fields.Integer(
        string="Total Votes", default=0, help="Total number of votes on this review"
    )

    helpfulness_ratio = fields.Float(
        string="Helpfulness Ratio",
        compute="_compute_helpfulness_ratio",
        store=True,
        help="Ratio of helpful votes to total votes",
    )

    # Moderation
    moderator_id = fields.Many2one(
        "res.users", string="Moderator", help="User who moderated this review"
    )

    moderation_date = fields.Datetime(
        string="Moderation Date", help="Date when review was moderated"
    )

    moderation_notes = fields.Text(
        string="Moderation Notes", help="Internal notes about review moderation"
    )

    # Response from Business
    business_response = fields.Text(
        string="Business Response", help="Response from the business to this review"
    )

    response_date = fields.Datetime(
        string="Response Date", help="Date when business responded"
    )

    response_user_id = fields.Many2one(
        "res.users",
        string="Response By",
        help="User who responded on behalf of the business",
    )

    @api.depends("rating")
    def _compute_rating_value(self):
        """Convert rating selection to numeric value."""
        for record in self:
            record.rating_value = float(record.rating) if record.rating else 0.0

    @api.depends("helpfulness_count", "total_votes")
    def _compute_helpfulness_ratio(self):
        """Calculate helpfulness ratio."""
        for record in self:
            if record.total_votes > 0:
                record.helpfulness_ratio = (
                    record.helpfulness_count / record.total_votes
                ) * 100
            else:
                record.helpfulness_ratio = 0.0

    def _compute_website_url(self):
        """Compute the website URL for this review."""
        for record in self:
            if record.id:
                record.website_url = f"/review/{record.id}"
            else:
                record.website_url = ""

    @api.constrains("rating")
    def _check_rating(self):
        """Validate rating value."""
        for record in self:
            if record.rating and record.rating not in ["1", "2", "3", "4", "5"]:
                raise ValidationError(_("Rating must be between 1 and 5 stars."))

    @api.constrains("customer_email")
    def _check_email(self):
        """Validate email format."""
        for record in self:
            if record.customer_email:
                import re

                email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
                if not re.match(email_pattern, record.customer_email):
                    raise ValidationError(_("Please enter a valid email address."))

    def action_submit(self):
        """Submit review for moderation."""
        for record in self:
            if record.state == "draft":
                record.write(
                    {
                        "state": "submitted",
                    }
                )
                record._send_notification_to_moderators()
                record.message_post(
                    body=_("Review has been submitted for moderation."),
                    message_type="notification",
                )

    def action_approve(self):
        """Approve review and publish on website."""
        for record in self:
            if record.state == "submitted":
                record.write(
                    {
                        "state": "approved",
                        "website_published": True,
                        "moderator_id": self.env.user.id,
                        "moderation_date": fields.Datetime.now(),
                    }
                )
                record._send_approval_notification()
                record.message_post(
                    body=_("Review has been approved and published on website."),
                    message_type="notification",
                )

    def action_reject(self):
        """Reject review."""
        for record in self:
            if record.state == "submitted":
                record.write(
                    {
                        "state": "rejected",
                        "website_published": False,
                        "moderator_id": self.env.user.id,
                        "moderation_date": fields.Datetime.now(),
                    }
                )
                record._send_rejection_notification()
                record.message_post(
                    body=_("Review has been rejected."), message_type="notification"
                )

    def action_archive(self):
        """Archive review."""
        for record in self:
            record.write(
                {
                    "state": "archived",
                    "website_published": False,
                }
            )
            record.message_post(
                body=_("Review has been archived."), message_type="notification"
            )

    def action_publish(self):
        """Publish review on website."""
        for record in self:
            if record.state == "approved":
                record.website_published = True
                record.message_post(
                    body=_("Review has been published on website."),
                    message_type="notification",
                )

    def action_unpublish(self):
        """Unpublish review from website."""
        for record in self:
            record.website_published = False
            record.message_post(
                body=_("Review has been unpublished from website."),
                message_type="notification",
            )

    def _send_notification_to_moderators(self):
        """Send notification to moderators when new review is submitted."""
        moderator_group = self.env.ref(
            "review_feedback_system.group_review_moderator", False
        )
        if moderator_group:
            moderators = moderator_group.users
            if moderators:
                self.activity_schedule(
                    "review_feedback_system.mail_activity_review_moderation",
                    user_id=moderators[0].id,
                    summary=_("New review submitted for moderation"),
                    note=_(
                        'A new review "%s" has been submitted and requires moderation.'
                    )
                    % self.title,
                )

    def _send_approval_notification(self):
        """Send notification when review is approved."""
        if self.customer_email:
            template = self.env.ref(
                "review_feedback_system.email_template_review_approved", False
            )
            if template:
                template.send_mail(self.id, force_send=True)

    def _send_rejection_notification(self):
        """Send notification when review is rejected."""
        if self.customer_email:
            template = self.env.ref(
                "review_feedback_system.email_template_review_rejected", False
            )
            if template:
                template.send_mail(self.id, force_send=True)

    def add_business_response(self, response_text):
        """Add business response to review."""
        self.write(
            {
                "business_response": response_text,
                "response_date": fields.Datetime.now(),
                "response_user_id": self.env.user.id,
            }
        )
        self.message_post(
            body=_("Business response has been added to the review."),
            message_type="notification",
        )

    @api.model
    def get_average_rating(self, product_id=None, category_id=None):
        """Get average rating for products or categories."""
        domain = [("state", "=", "approved"), ("website_published", "=", True)]

        if product_id:
            domain.append(("product_id", "=", product_id))
        if category_id:
            domain.append(("category_id", "=", category_id))

        reviews = self.search(domain)
        if reviews:
            return sum(float(review.rating) for review in reviews) / len(reviews)
        return 0

    @api.model
    def get_review_stats(self, product_id=None, category_id=None):
        """Get comprehensive review statistics."""
        domain = [("state", "=", "approved"), ("website_published", "=", True)]

        if product_id:
            domain.append(("product_id", "=", product_id))
        if category_id:
            domain.append(("category_id", "=", category_id))

        reviews = self.search(domain)

        stats = {
            "total_reviews": len(reviews),
            "average_rating": 0,
            "rating_distribution": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0},
            "recommendation_rate": 0,
        }

        if reviews:
            stats["average_rating"] = sum(
                float(review.rating) for review in reviews
            ) / len(reviews)

            for review in reviews:
                stats["rating_distribution"][review.rating] += 1

            recommended_count = len(reviews.filtered("recommend"))
            stats["recommendation_rate"] = (
                (recommended_count / len(reviews)) * 100 if reviews else 0
            )

        return stats

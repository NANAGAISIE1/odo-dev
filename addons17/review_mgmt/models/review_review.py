# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.tools import html2plaintext


class ReviewReview(models.Model):
    _name = "review.review"
    _description = "Review"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(string="Title")
    sequence = fields.Char(
        string="Ref",
        default=lambda self: self.env["ir.sequence"].next_by_code("review.review"),
    )
    listing_id = fields.Many2one(
        "review.listing", required=True, ondelete="cascade", index=True, tracking=True
    )

    platform = fields.Selection(related="listing_id.platform", store=True)
    author_name = fields.Char(required=True, tracking=True)
    author_email = fields.Char()
    rating = fields.Integer(default=5, required=True)
    content = fields.Html(required=True, sanitize=True)
    content_text = fields.Text(compute="_compute_content_text", store=True)
    date = fields.Datetime(default=fields.Datetime.now, required=True, index=True)

    state = fields.Selection(
        [
            ("new", "New"),
            ("in_progress", "In Progress"),
            ("responded", "Responded"),
            ("archived", "Archived"),
        ],
        default="new",
        tracking=True,
    )

    sentiment = fields.Selection(
        [
            ("positive", "Positive"),
            ("neutral", "Neutral"),
            ("negative", "Negative"),
        ],
        compute="_compute_sentiment",
        store=True,
    )

    response_ids = fields.One2many("review.response", "review_id", string="Responses")
    response_count = fields.Integer(compute="_compute_response_count", store=True)

    @api.constrains("rating")
    def _check_rating_range(self):
        for rec in self:
            if rec.rating < 1 or rec.rating > 5:
                raise ValueError(_("Rating must be between 1 and 5."))

    @api.depends("content")
    def _compute_content_text(self):
        for rec in self:
            rec.content_text = html2plaintext(rec.content or "")

    @api.depends("content_text")
    def _compute_sentiment(self):
        # naive rule-based MVP
        positive_words = {
            "good",
            "great",
            "excellent",
            "love",
            "amazing",
            "fast",
            "happy",
        }
        negative_words = {
            "bad",
            "poor",
            "terrible",
            "hate",
            "slow",
            "broken",
            "unhappy",
        }
        for rec in self:
            text = (rec.content_text or "").lower()
            pos = sum(1 for w in positive_words if w in text)
            neg = sum(1 for w in negative_words if w in text)
            if pos > neg:
                rec.sentiment = "positive"
            elif neg > pos:
                rec.sentiment = "negative"
            else:
                rec.sentiment = "neutral"

    @api.depends("response_ids")
    def _compute_response_count(self):
        for rec in self:
            rec.response_count = len(rec.response_ids)

    def action_post_chatter_message(self):
        for rec in self:
            rec.message_post(
                body=f"New review by {rec.author_name} (Rating: {rec.rating}/5)"
            )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            # Notify in chatter for visibility
            rec.message_post(
                body=_("New review created by %s (Rating: %s/5)")
                % (rec.author_name or _("Unknown"), rec.rating),
                message_type="notification",
                subtype_xmlid="mail.mt_note",
            )
            # Schedule an activity when negative
            if rec.sentiment == "negative":
                rec._schedule_negative_review_activity()
        return records

    def write(self, vals):
        res = super().write(vals)
        # after write, if sentiment becomes negative, schedule activity
        for rec in self:
            if rec.sentiment == "negative":
                rec._schedule_negative_review_activity()
        return res

    def _schedule_negative_review_activity(self):
        for rec in self:
            # Avoid creating duplicates: only one pending activity of this type
            existing = rec.activity_ids.filtered(
                lambda a: a.summary == "Follow up negative review"
            )
            if existing:
                continue
            rec.activity_schedule(
                "mail.mail_activity_data_todo",
                user_id=self.env.user.id,
                note=_("Review by %s rated %s/5. Please follow up.")
                % (rec.author_name or _("Unknown"), rec.rating),
                summary=_("Follow up negative review"),
            )

    @api.model
    def _cron_fetch_external_reviews(self):
        """Placeholder to fetch new reviews from external platforms.
        Implement connectors and create review.review records here.
        """
        return True


class ReviewResponse(models.Model):
    _name = "review.response"
    _description = "Review Response"
    _inherit = ["mail.thread"]

    review_id = fields.Many2one(
        "review.review", required=True, ondelete="cascade", index=True
    )
    author_id = fields.Many2one(
        "res.users", default=lambda self: self.env.user, required=True
    )
    body = fields.Html(required=True)
    template_id = fields.Many2one("review.response.template")
    posted = fields.Boolean(
        default=False, help="Whether the response was posted to the source platform"
    )

    def action_send_response(self):
        for rec in self:
            # Post in chatter and mark as responded
            rec.review_id.message_post(
                body=rec.body,
                body_is_html=True,
                message_type="comment",
                subtype_xmlid="mail.mt_comment",
            )
            rec.review_id.state = "responded"
            rec.posted = True
            # hook: real platform integration would go here
            # self.env['review.platform.connector']._send_response(rec)

    # Response template is defined in its own model file

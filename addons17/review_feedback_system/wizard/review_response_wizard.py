from odoo import _, api, fields, models


class ReviewResponseWizard(models.TransientModel):
    _name = "review.response.wizard"
    _description = "Review Response Wizard"

    review_id = fields.Many2one("review.feedback", string="Review", required=True)

    response_text = fields.Text(
        string="Business Response", required=True, help="Your response to this review"
    )

    notify_customer = fields.Boolean(
        string="Notify Customer",
        default=True,
        help="Send email notification to customer about your response",
    )

    @api.model
    def default_get(self, fields_list):
        """Set default values from context."""
        res = super().default_get(fields_list)

        # Get active review from context
        active_id = self.env.context.get("active_id")
        if active_id:
            res["review_id"] = active_id

        return res

    def action_submit_response(self):
        """Submit business response to review."""
        self.ensure_one()

        # Add response to review
        self.review_id.add_business_response(self.response_text)

        # Send notification if requested
        if self.notify_customer and self.review_id.customer_email:
            self._send_response_notification()

        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

    def _send_response_notification(self):
        """Send email notification to customer about business response."""
        template = self.env.ref(
            "review_feedback_system.email_template_business_response", False
        )

        if template:
            template.send_mail(self.review_id.id, force_send=True)

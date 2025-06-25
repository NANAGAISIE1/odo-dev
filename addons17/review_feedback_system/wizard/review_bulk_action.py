from odoo import _, api, fields, models


class ReviewBulkAction(models.TransientModel):
    _name = "review.bulk.action"
    _description = "Review Bulk Action Wizard"

    action_type = fields.Selection(
        [
            ("approve", "Approve Reviews"),
            ("reject", "Reject Reviews"),
            ("archive", "Archive Reviews"),
            ("publish", "Publish on Website"),
            ("unpublish", "Unpublish from Website"),
        ],
        string="Action",
        required=True,
    )

    review_ids = fields.Many2many("review.feedback", string="Reviews", required=True)

    reason = fields.Text(string="Reason", help="Reason for this action (optional)")

    @api.model
    def default_get(self, fields_list):
        """Set default values from context."""
        res = super().default_get(fields_list)

        # Get active reviews from context
        active_ids = self.env.context.get("active_ids", [])
        if active_ids:
            res["review_ids"] = [(6, 0, active_ids)]

        return res

    def action_execute(self):
        """Execute the bulk action on selected reviews."""
        for review in self.review_ids:
            if self.action_type == "approve":
                if review.state == "submitted":
                    review.action_approve()
                    if self.reason:
                        review.message_post(
                            body=_("Bulk approval reason: %s") % self.reason,
                            message_type="comment",
                        )

            elif self.action_type == "reject":
                if review.state == "submitted":
                    review.action_reject()
                    if self.reason:
                        review.message_post(
                            body=_("Bulk rejection reason: %s") % self.reason,
                            message_type="comment",
                        )

            elif self.action_type == "archive":
                review.action_archive()
                if self.reason:
                    review.message_post(
                        body=_("Bulk archive reason: %s") % self.reason,
                        message_type="comment",
                    )

            elif self.action_type == "publish":
                if review.state == "approved":
                    review.action_publish()

            elif self.action_type == "unpublish":
                review.action_unpublish()

        return {
            "type": "ir.actions.client",
            "tag": "reload",
        }

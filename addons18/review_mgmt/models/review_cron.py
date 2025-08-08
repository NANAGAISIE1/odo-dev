# -*- coding: utf-8 -*-
from odoo import models


class ReviewReviewCron(models.AbstractModel):
    _name = "review.review.cron"
    _description = "Review Cron Helpers"

    def _cron_fetch_external_reviews(self):
        # Placeholder: implement connectors and fetching pipeline
        return True

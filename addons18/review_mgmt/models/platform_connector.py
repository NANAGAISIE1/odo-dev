# -*- coding: utf-8 -*-
from odoo import models


class ReviewPlatformConnector(models.AbstractModel):
    _name = "review.platform.connector"
    _description = "Review Platform Connector (abstract)"

    def _send_response(self, response_record):
        """Override in real connectors to send response to a platform"""
        return True

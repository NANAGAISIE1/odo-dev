# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class ReviewApiController(http.Controller):
    @http.route("/review_mgmt/api/reviews", type="json", auth="user", methods=["POST"])
    def create_review(self, **payload):
        # Minimal secure endpoint to create reviews (manual input or 3rd party)
        vals = {
            "listing_id": payload.get("listing_id"),
            "author_name": payload.get("author_name"),
            "author_email": payload.get("author_email"),
            "rating": payload.get("rating", 5),
            "content": payload.get("content"),
            "date": payload.get("date"),
        }
        rec = request.env["review.review"].sudo().create(vals)
        return {"id": rec.id, "sequence": rec.sequence}

    @http.route(
        "/review_mgmt/api/reviews/<int:review_id>/respond",
        type="json",
        auth="user",
        methods=["POST"],
    )
    def respond_review(self, review_id, **payload):
        body = payload.get("body")
        rec = request.env["review.review"].sudo().browse(review_id)
        rec.ensure_one()
        response = (
            request.env["review.response"]
            .sudo()
            .create(
                {
                    "review_id": rec.id,
                    "body": body,
                }
            )
        )
        response.action_send_response()
        return {"ok": True}

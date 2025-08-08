# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestReviewFlow(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.listing = cls.env["review.listing"].create(
            {
                "name": "Demo Product",
                "listing_type": "product",
                "platform": "manual",
            }
        )

    def test_create_review_and_respond(self):
        review = self.env["review.review"].create(
            {
                "listing_id": self.listing.id,
                "author_name": "Alice",
                "rating": 2,
                "content": "<p>bad and slow</p>",
            }
        )
        self.assertTrue(review.sentiment in ("negative", "neutral", "positive"))
        self.env["review.response"].create(
            {
                "review_id": review.id,
                "body": "<p>Thanks for your feedback</p>",
            }
        ).action_send_response()
        self.assertEqual(review.state, "responded")

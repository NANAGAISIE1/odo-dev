import logging

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged

_logger = logging.getLogger(__name__)


@tagged("review_system")
class TestReviewFeedbackSystem(TransactionCase):
    """Test cases for the Review and Feedback System."""

    def setUp(self):
        super().setUp()

        # Create test data
        self.partner = self.env["res.partner"].create(
            {
                "name": "Test Customer",
                "email": "test@example.com",
                "customer_rank": 1,
            }
        )

        self.product = self.env["product.template"].create(
            {
                "name": "Test Product",
                "type": "consu",
                "sale_ok": True,
                "list_price": 100.0,
            }
        )

        self.category = self.env["review.category"].create(
            {
                "name": "Test Category",
                "description": "Test category for reviews",
                "website_published": True,
                "active": True,
            }
        )

        self.review_data = {
            "title": "Great Product",
            "content": "This is an excellent product with great quality.",
            "rating": "5",
            "partner_id": self.partner.id,
            "customer_name": self.partner.name,
            "customer_email": self.partner.email,
            "product_id": self.product.id,
            "category_id": self.category.id,
            "pros": "Excellent quality, fast delivery",
            "cons": "A bit expensive",
            "recommend": True,
            "verified_purchase": True,
        }

    def test_review_creation(self):
        """Test basic review creation."""
        review = self.env["review.feedback"].create(self.review_data)

        self.assertEqual(review.state, "draft")
        self.assertEqual(review.rating_value, 5.0)
        self.assertFalse(review.website_published)
        self.assertTrue(review.recommend)

    def test_review_workflow(self):
        """Test review state transitions."""
        review = self.env["review.feedback"].create(self.review_data)

        # Submit review
        review.action_submit()
        self.assertEqual(review.state, "submitted")

        # Approve review
        review.action_approve()
        self.assertEqual(review.state, "approved")
        self.assertTrue(review.website_published)

        # Unpublish review
        review.action_unpublish()
        self.assertFalse(review.website_published)

        # Archive review
        review.action_archive()
        self.assertEqual(review.state, "archived")

    def test_review_rejection(self):
        """Test review rejection workflow."""
        review = self.env["review.feedback"].create(self.review_data)
        review.action_submit()

        # Reject review
        review.action_reject()
        self.assertEqual(review.state, "rejected")
        self.assertFalse(review.website_published)

    def test_review_validation(self):
        """Test review field validation."""
        # Test missing required fields
        with self.assertRaises(ValidationError):
            self.env["review.feedback"].create(
                {
                    "content": "Test content",
                    "rating": "5",
                }
            )

    def test_email_validation(self):
        """Test email field validation."""
        invalid_review_data = self.review_data.copy()
        invalid_review_data["customer_email"] = "invalid-email"

        review = self.env["review.feedback"].create(invalid_review_data)
        with self.assertRaises(ValidationError):
            review._check_email()

    def test_rating_value_computation(self):
        """Test rating value computation."""
        review = self.env["review.feedback"].create(self.review_data)
        self.assertEqual(review.rating_value, 5.0)

        review.rating = "3"
        self.assertEqual(review.rating_value, 3.0)

    def test_helpfulness_ratio_computation(self):
        """Test helpfulness ratio computation."""
        review = self.env["review.feedback"].create(self.review_data)

        # No votes initially
        self.assertEqual(review.helpfulness_ratio, 0.0)

        # Add some votes
        review.write(
            {
                "helpfulness_count": 8,
                "total_votes": 10,
            }
        )
        self.assertEqual(review.helpfulness_ratio, 80.0)

    def test_website_url_computation(self):
        """Test website URL computation."""
        review = self.env["review.feedback"].create(self.review_data)
        expected_url = f"/review/{review.id}"
        self.assertEqual(review.website_url, expected_url)

    def test_business_response(self):
        """Test business response functionality."""
        review = self.env["review.feedback"].create(self.review_data)
        response_text = "Thank you for your review!"

        review.add_business_response(response_text)

        self.assertEqual(review.business_response, response_text)
        self.assertIsNotNone(review.response_date)
        self.assertEqual(review.response_user_id, self.env.user)

    def test_review_category(self):
        """Test review category functionality."""
        # Test category creation
        category = self.env["review.category"].create(
            {
                "name": "Electronics",
                "description": "Electronic products",
                "website_published": True,
                "active": True,
                "color": 1,
            }
        )

        self.assertTrue(category.active)
        self.assertTrue(category.website_published)

        # Test review count computation
        review1 = self.env["review.feedback"].create(self.review_data)
        review2_data = self.review_data.copy()
        review2_data["title"] = "Another Review"
        review2_data["category_id"] = category.id
        review2 = self.env["review.feedback"].create(review2_data)

        category._compute_review_stats()
        self.assertEqual(category.review_count, 1)

    def test_partner_review_stats(self):
        """Test partner review statistics."""
        # Create multiple reviews for the partner
        review1 = self.env["review.feedback"].create(self.review_data)

        review2_data = self.review_data.copy()
        review2_data["title"] = "Another Great Product"
        review2_data["rating"] = "4"
        review2 = self.env["review.feedback"].create(review2_data)

        self.partner._compute_review_count()
        self.partner._compute_average_rating_given()

        self.assertEqual(self.partner.review_count, 2)
        self.assertEqual(self.partner.average_rating_given, 4.5)

    def test_product_review_integration(self):
        """Test product and review integration."""
        review = self.env["review.feedback"].create(self.review_data)

        # Test that product has review stats
        self.product._compute_review_stats()
        self.assertEqual(self.product.review_count, 1)
        self.assertEqual(self.product.average_rating, 5.0)

    def test_review_settings(self):
        """Test review settings functionality."""
        settings = self.env["review.settings"].create(
            {
                "require_moderation": True,
                "allow_anonymous_reviews": True,
                "min_rating_to_publish": "3",
                "notify_on_new_review": True,
                "reviews_per_page": 15,
            }
        )

        # Test settings save and load
        settings.set_values()

        # Verify parameters were set
        params = self.env["ir.config_parameter"].sudo()
        self.assertEqual(
            params.get_param("review_feedback_system.require_moderation"), "True"
        )
        self.assertEqual(
            params.get_param("review_feedback_system.min_rating_publish"), "3"
        )

    def test_anonymous_review(self):
        """Test anonymous review creation."""
        anonymous_data = {
            "title": "Anonymous Review",
            "content": "This is an anonymous review.",
            "rating": "4",
            "customer_name": "Anonymous User",
            "customer_email": "anon@example.com",
            "is_anonymous": True,
            "product_id": self.product.id,
            "category_id": self.category.id,
        }

        review = self.env["review.feedback"].create(anonymous_data)
        self.assertTrue(review.is_anonymous)
        self.assertFalse(review.partner_id)

    def test_review_bulk_actions(self):
        """Test bulk actions on reviews."""
        # Create multiple reviews
        reviews = self.env["review.feedback"]
        for i in range(3):
            review_data = self.review_data.copy()
            review_data["title"] = f"Review {i + 1}"
            review = self.env["review.feedback"].create(review_data)
            review.action_submit()
            reviews |= review

        # Test bulk approval
        bulk_action = self.env["review.bulk.action"].create(
            {
                "action_type": "approve",
                "review_ids": [(6, 0, reviews.ids)],
                "notify_customers": False,
            }
        )

        bulk_action.action_execute()

        # Verify all reviews are approved
        for review in reviews:
            self.assertEqual(review.state, "approved")

    def test_review_response_wizard(self):
        """Test review response wizard."""
        review = self.env["review.feedback"].create(self.review_data)

        wizard = self.env["review.response.wizard"].create(
            {
                "review_id": review.id,
                "response_text": "Thank you for your feedback!",
                "notify_customer": False,
            }
        )

        wizard.action_submit_response()

        self.assertEqual(review.business_response, "Thank you for your feedback!")
        self.assertIsNotNone(review.response_date)

    def test_review_analytics(self):
        """Test review analytics functionality."""
        # Create reviews with different ratings
        ratings = ["5", "4", "3", "2", "1"]
        for rating in ratings:
            review_data = self.review_data.copy()
            review_data["rating"] = rating
            review_data["title"] = f"Review with {rating} stars"
            review = self.env["review.feedback"].create(review_data)
            review.action_submit()
            review.action_approve()

        # Update analytics
        analytics = self.env["review.analytics"].sudo()
        analytics.update_analytics()

        # Check analytics for the product
        product_analytics = analytics.search([("product_id", "=", self.product.id)])

        self.assertTrue(product_analytics)
        self.assertEqual(product_analytics.total_reviews, 5)
        self.assertEqual(product_analytics.average_rating, 3.0)

    def test_review_search_and_filtering(self):
        """Test review search functionality."""
        # Create reviews with different attributes
        review1 = self.env["review.feedback"].create(self.review_data)
        review1.action_submit()
        review1.action_approve()

        review2_data = self.review_data.copy()
        review2_data["title"] = "Poor Product"
        review2_data["rating"] = "2"
        review2_data["recommend"] = False
        review2 = self.env["review.feedback"].create(review2_data)
        review2.action_submit()
        review2.action_approve()

        # Test search by rating
        high_rated = self.env["review.feedback"].search(
            [("rating_value", ">=", 4), ("state", "=", "approved")]
        )
        self.assertIn(review1, high_rated)
        self.assertNotIn(review2, high_rated)

        # Test search by recommendation
        recommended = self.env["review.feedback"].search(
            [("recommend", "=", True), ("state", "=", "approved")]
        )
        self.assertIn(review1, recommended)
        self.assertNotIn(review2, recommended)

    def test_review_security(self):
        """Test review security and access rights."""
        # Create a portal user
        portal_user = self.env["res.users"].create(
            {
                "name": "Portal User",
                "login": "portal@example.com",
                "email": "portal@example.com",
                "groups_id": [(6, 0, [self.env.ref("base.group_portal").id])],
                "partner_id": self.partner.id,
            }
        )

        # Test that portal user can only see their own reviews
        review = (
            self.env["review.feedback"]
            .with_user(portal_user)
            .create(
                {
                    "title": "My Review",
                    "content": "This is my review.",
                    "rating": "5",
                    "partner_id": self.partner.id,
                    "customer_name": self.partner.name,
                    "customer_email": self.partner.email,
                }
            )
        )

        # Portal user should be able to read their own review
        self.assertTrue(review.with_user(portal_user).exists())

        # But not modify state directly
        with self.assertRaises(Exception):
            review.with_user(portal_user).write({"state": "approved"})

    def tearDown(self):
        """Clean up test data."""
        super().tearDown()
        # Clean up is handled automatically by TransactionCase

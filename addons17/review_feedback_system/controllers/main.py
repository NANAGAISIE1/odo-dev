import logging

from odoo import _, http
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class ReviewController(http.Controller):
    @http.route("/reviews", type="http", auth="public", website=True, sitemap=True)
    def reviews_list(
        self, page=1, category=None, product=None, rating=None, search=None, **kwargs
    ):
        """Display list of reviews on website."""
        ReviewFeedback = request.env["review.feedback"]
        ReviewCategory = request.env["review.category"]

        # Get settings
        reviews_per_page = int(
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("review_feedback_system.reviews_per_page", 10)
        )

        # Build domain
        domain = [("state", "=", "approved"), ("website_published", "=", True)]

        if category:
            domain.append(("category_id", "=", int(category)))
        if product:
            domain.append(("product_id", "=", int(product)))
        if rating:
            domain.append(("rating", "=", rating))
        if search:
            domain.extend(
                [
                    "|",
                    "|",
                    "|",
                    ("title", "ilike", search),
                    ("content", "ilike", search),
                    ("customer_name", "ilike", search),
                    ("pros", "ilike", search),
                ]
            )

        # Get reviews
        total_reviews = ReviewFeedback.search_count(domain)

        pager = request.website.pager(
            url="/reviews",
            url_args=kwargs,
            total=total_reviews,
            page=page,
            step=reviews_per_page,
        )

        reviews = ReviewFeedback.search(
            domain,
            limit=reviews_per_page,
            offset=pager["offset"],
            order="create_date desc",
        )

        # Get categories for filter
        categories = ReviewCategory.search(
            [("website_published", "=", True), ("active", "=", True)],
            order="website_sequence, name",
        )

        # Get products for filter
        products = request.env["product.template"].search(
            [("id", "in", reviews.mapped("product_id").ids)]
        )

        values = {
            "reviews": reviews,
            "categories": categories,
            "products": products,
            "pager": pager,
            "search": search,
            "current_category": int(category) if category else None,
            "current_product": int(product) if product else None,
            "current_rating": rating,
            "total_reviews": total_reviews,
        }

        return request.render("review_feedback_system.reviews_list_template", values)

    @http.route("/review/<int:review_id>", type="http", auth="public", website=True)
    def review_detail(self, review_id, **kwargs):
        """Display individual review detail."""
        review = request.env["review.feedback"].search(
            [
                ("id", "=", review_id),
                ("state", "=", "approved"),
                ("website_published", "=", True),
            ],
            limit=1,
        )

        if not review:
            return request.not_found()

        # Get related reviews
        related_reviews = request.env["review.feedback"].search(
            [
                ("product_id", "=", review.product_id.id),
                ("state", "=", "approved"),
                ("website_published", "=", True),
                ("id", "!=", review.id),
            ],
            limit=5,
            order="create_date desc",
        )

        values = {
            "review": review,
            "related_reviews": related_reviews,
        }

        return request.render("review_feedback_system.review_detail_template", values)

    @http.route(
        "/review/submit",
        type="http",
        auth="public",
        website=True,
        methods=["GET", "POST"],
    )
    def submit_review(self, **kwargs):
        """Handle review submission."""
        if request.httprequest.method == "POST":
            return self._process_review_submission(**kwargs)

        # GET request - show form
        products = request.env["product.template"].search(
            [("sale_ok", "=", True)], order="name"
        )

        categories = request.env["review.category"].search(
            [("website_published", "=", True), ("active", "=", True)],
            order="website_sequence, name",
        )

        values = {
            "products": products,
            "categories": categories,
        }

        return request.render("review_feedback_system.review_submit_template", values)

    def _process_review_submission(self, **kwargs):
        """Process review form submission."""
        try:
            # Validate required fields
            required_fields = ["title", "content", "rating"]
            for field in required_fields:
                if not kwargs.get(field):
                    raise ValidationError(_("Please fill in all required fields."))

            # Check anonymous reviews setting
            allow_anonymous = (
                request.env["ir.config_parameter"]
                .sudo()
                .get_param("review_feedback_system.allow_anonymous", True)
            )

            user = request.env.user
            partner_id = None
            customer_name = None
            customer_email = None

            if user and not user._is_public():
                partner_id = user.partner_id.id
            elif allow_anonymous:
                customer_name = kwargs.get("customer_name")
                customer_email = kwargs.get("customer_email")
                if not customer_name or not customer_email:
                    raise ValidationError(_("Please provide your name and email."))
            else:
                return request.redirect("/web/login?redirect=/review/submit")

            # Create review
            review_data = {
                "title": kwargs.get("title"),
                "content": kwargs.get("content"),
                "rating": kwargs.get("rating"),
                "pros": kwargs.get("pros", ""),
                "cons": kwargs.get("cons", ""),
                "recommend": kwargs.get("recommend") == "on",
                "partner_id": partner_id,
                "customer_name": customer_name,
                "customer_email": customer_email,
                "is_anonymous": not partner_id,
                "product_id": int(kwargs.get("product_id"))
                if kwargs.get("product_id")
                else None,
                "category_id": int(kwargs.get("category_id"))
                if kwargs.get("category_id")
                else None,
                "state": "submitted",
            }

            review = request.env["review.feedback"].sudo().create(review_data)

            # Handle file attachments
            if "attachments" in request.httprequest.files:
                self._handle_attachments(
                    review, request.httprequest.files.getlist("attachments")
                )

            # Send notification
            review.action_submit()

            # Redirect to success page
            return request.redirect(f"/review/thank-you?review_id={review.id}")

        except ValidationError as e:
            # Handle validation errors
            error_message = str(e)
            products = request.env["product.template"].search(
                [("sale_ok", "=", True)], order="name"
            )
            categories = request.env["review.category"].search(
                [("website_published", "=", True), ("active", "=", True)],
                order="website_sequence, name",
            )

            values = {
                "products": products,
                "categories": categories,
                "error_message": error_message,
                "form_data": kwargs,
            }

            return request.render(
                "review_feedback_system.review_submit_template", values
            )

        except Exception as e:
            _logger.error(f"Error submitting review: {str(e)}")
            return request.redirect("/review/submit?error=1")

    def _handle_attachments(self, review, files):
        """Handle file attachments for review."""
        for file in files:
            if file.filename:
                attachment = (
                    request.env["ir.attachment"]
                    .sudo()
                    .create(
                        {
                            "name": file.filename,
                            "datas": file.read(),
                            "res_model": "review.feedback",
                            "res_id": review.id,
                            "public": True,
                        }
                    )
                )
                review.attachment_ids = [(4, attachment.id)]

    @http.route("/review/thank-you", type="http", auth="public", website=True)
    def review_thank_you(self, review_id=None, **kwargs):
        """Thank you page after review submission."""
        review = None
        if review_id:
            review = request.env["review.feedback"].sudo().browse(int(review_id))

        values = {
            "review": review,
        }

        return request.render(
            "review_feedback_system.review_thank_you_template", values
        )

    @http.route("/review/vote", type="json", auth="public", methods=["POST"])
    def vote_review(self, review_id, helpful=True):
        """Handle review voting."""
        try:
            # Check if voting is allowed
            allow_voting = (
                request.env["ir.config_parameter"]
                .sudo()
                .get_param("review_feedback_system.allow_voting", True)
            )

            if not allow_voting:
                return {"error": _("Voting is not enabled.")}

            review = request.env["review.feedback"].sudo().browse(review_id)
            if not review.exists():
                return {"error": _("Review not found.")}

            # Update vote counts
            if helpful:
                review.helpfulness_count += 1
            review.total_votes += 1

            return {
                "success": True,
                "helpfulness_count": review.helpfulness_count,
                "total_votes": review.total_votes,
                "helpfulness_ratio": review.helpfulness_ratio,
            }

        except Exception as e:
            _logger.error(f"Error voting on review: {str(e)}")
            return {"error": _("An error occurred while voting.")}

    @http.route("/reviews/api/stats", type="json", auth="public")
    def get_review_stats(self, product_id=None, category_id=None):
        """API endpoint to get review statistics."""
        try:
            stats = request.env["review.feedback"].get_review_stats(
                product_id=product_id, category_id=category_id
            )
            return stats
        except Exception as e:
            _logger.error(f"Error getting review stats: {str(e)}")
            return {"error": str(e)}

    @http.route(
        "/reviews/product/<int:product_id>", type="http", auth="public", website=True
    )
    def product_reviews(self, product_id, page=1, **kwargs):
        """Display reviews for a specific product."""
        product = request.env["product.template"].browse(product_id)
        if not product.exists():
            return request.not_found()

        # Get reviews for this product
        domain = [
            ("product_id", "=", product_id),
            ("state", "=", "approved"),
            ("website_published", "=", True),
        ]

        reviews_per_page = int(
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("review_feedback_system.reviews_per_page", 10)
        )

        total_reviews = request.env["review.feedback"].search_count(domain)

        pager = request.website.pager(
            url=f"/reviews/product/{product_id}",
            total=total_reviews,
            page=page,
            step=reviews_per_page,
        )

        reviews = request.env["review.feedback"].search(
            domain,
            limit=reviews_per_page,
            offset=pager["offset"],
            order="create_date desc",
        )

        # Get product stats
        stats = request.env["review.feedback"].get_review_stats(product_id=product_id)

        values = {
            "product": product,
            "reviews": reviews,
            "pager": pager,
            "stats": stats,
            "total_reviews": total_reviews,
        }

        return request.render("review_feedback_system.product_reviews_template", values)

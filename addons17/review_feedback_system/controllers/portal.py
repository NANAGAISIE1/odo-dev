import logging

from odoo import _, http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request

_logger = logging.getLogger(__name__)


class ReviewPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        """Add review count to portal home."""
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        if "review_count" in counters:
            review_count = (
                request.env["review.feedback"].search_count(
                    [("partner_id", "=", partner.id)]
                )
                if partner
                else 0
            )
            values["review_count"] = review_count

        return values

    @http.route(
        ["/my/reviews", "/my/reviews/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_reviews(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        search=None,
        search_in="title",
        **kw,
    ):
        """Display customer's reviews in portal."""
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        ReviewFeedback = request.env["review.feedback"]

        # Build domain
        domain = [("partner_id", "=", partner.id)]

        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]

        if search and search_in:
            search_domain = []
            if search_in in ("title", "all"):
                search_domain.append(("title", "ilike", search))
            if search_in in ("content", "all"):
                search_domain.append(("content", "ilike", search))
            if search_in == "all":
                search_domain = ["|"] * (len(search_domain) - 1) + search_domain
            domain += search_domain

        # Sorting options
        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Title"), "order": "title"},
            "rating": {"label": _("Rating"), "order": "rating desc"},
            "state": {"label": _("Status"), "order": "state"},
        }

        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]

        # Search options
        searchbar_inputs = {
            "title": {"input": "title", "label": _("Search in Title")},
            "content": {"input": "content", "label": _("Search in Content")},
            "all": {"input": "all", "label": _("Search in All")},
        }

        # Paging
        review_count = ReviewFeedback.search_count(domain)
        pager = request.website.pager(
            url="/my/reviews",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "search": search,
                "search_in": search_in,
            },
            total=review_count,
            page=page,
            step=self._items_per_page,
        )

        # Get reviews
        reviews = ReviewFeedback.search(
            domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "reviews": reviews,
                "page_name": "review",
                "pager": pager,
                "default_url": "/my/reviews",
                "search_in": search_in,
                "search": search,
                "sortby": sortby,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_inputs": searchbar_inputs,
            }
        )

        return request.render("review_feedback_system.portal_my_reviews", values)

    @http.route(["/my/review/<int:review_id>"], type="http", auth="user", website=True)
    def portal_review_detail(self, review_id=None, **kw):
        """Display review detail in portal."""
        review = request.env["review.feedback"].browse(review_id)

        # Check access rights
        if not review or review.partner_id != request.env.user.partner_id:
            return request.not_found()

        values = {
            "review": review,
            "page_name": "review",
        }

        return request.render("review_feedback_system.portal_review_detail", values)

    @http.route(
        ["/my/review/<int:review_id>/edit"],
        type="http",
        auth="user",
        website=True,
        methods=["GET", "POST"],
    )
    def portal_review_edit(self, review_id=None, **kw):
        """Edit review in portal."""
        review = request.env["review.feedback"].browse(review_id)

        # Check access rights and editability
        if (
            not review
            or review.partner_id != request.env.user.partner_id
            or review.state not in ["draft", "submitted"]
        ):
            return request.not_found()

        if request.httprequest.method == "POST":
            return self._process_portal_review_edit(review, **kw)

        # GET request - show form
        products = request.env["product.template"].search(
            [("sale_ok", "=", True)], order="name"
        )

        categories = request.env["review.category"].search(
            [("website_published", "=", True), ("active", "=", True)],
            order="website_sequence, name",
        )

        values = {
            "review": review,
            "products": products,
            "categories": categories,
            "page_name": "review",
        }

        return request.render("review_feedback_system.portal_review_edit", values)

    def _process_portal_review_edit(self, review, **kw):
        """Process review edit form."""
        try:
            # Update review
            update_data = {}

            if kw.get("title"):
                update_data["title"] = kw.get("title")
            if kw.get("content"):
                update_data["content"] = kw.get("content")
            if kw.get("rating"):
                update_data["rating"] = kw.get("rating")
            if "pros" in kw:
                update_data["pros"] = kw.get("pros", "")
            if "cons" in kw:
                update_data["cons"] = kw.get("cons", "")
            if "recommend" in kw:
                update_data["recommend"] = kw.get("recommend") == "on"
            if kw.get("product_id"):
                update_data["product_id"] = int(kw.get("product_id"))
            if kw.get("category_id"):
                update_data["category_id"] = int(kw.get("category_id"))

            review.write(update_data)

            return request.redirect(f"/my/review/{review.id}?message=updated")

        except Exception as e:
            _logger.error(f"Error updating review: {str(e)}")
            return request.redirect(f"/my/review/{review.id}/edit?error=1")

    @http.route(
        ["/my/review/new"],
        type="http",
        auth="user",
        website=True,
        methods=["GET", "POST"],
    )
    def portal_review_new(self, **kw):
        """Create new review in portal."""
        if request.httprequest.method == "POST":
            return self._process_portal_review_new(**kw)

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
            "page_name": "review",
        }

        return request.render("review_feedback_system.portal_review_new", values)

    def _process_portal_review_new(self, **kw):
        """Process new review creation."""
        try:
            partner = request.env.user.partner_id

            # Create review
            review_data = {
                "title": kw.get("title"),
                "content": kw.get("content"),
                "rating": kw.get("rating"),
                "pros": kw.get("pros", ""),
                "cons": kw.get("cons", ""),
                "recommend": kw.get("recommend") == "on",
                "partner_id": partner.id,
                "product_id": int(kw.get("product_id"))
                if kw.get("product_id")
                else None,
                "category_id": int(kw.get("category_id"))
                if kw.get("category_id")
                else None,
                "state": "submitted",
            }

            review = request.env["review.feedback"].create(review_data)
            review.action_submit()

            return request.redirect(f"/my/review/{review.id}?message=created")

        except Exception as e:
            _logger.error(f"Error creating review: {str(e)}")
            return request.redirect("/my/review/new?error=1")

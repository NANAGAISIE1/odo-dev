Review Management (Odoo 17)
===========================

A lightweight app to collect, manage, respond to, and analyze reviews in Odoo 17.

Main features
-------------
- Listings (products/services) with review rollups (avg rating, count)
- Review records with chatter, activities, and naive sentiment analysis
- Response management with templates and one-click post to chatter
- Dashboards (graph + pivot) for trends and KPIs
- Basic PDF report for a single review (QWeb)
- JSON endpoints for ingestion and replies (authenticated)
- Placeholder cron + connector hooks for external platforms

Install
-------
1) Ensure addons path contains ``/mnt/extra-addons`` (Docker here mounts ``./addons17`` there).
2) Update Apps list and install "Review Management".

JSON API (MVP)
--------------
- Create review (auth user): ``/review_mgmt/api/reviews`` (JSON POST)
  payload keys: listing_id, author_name, author_email, rating, content, date
- Respond to review: ``/review_mgmt/api/reviews/<id>/respond`` (JSON POST)
  payload keys: body

Notes
-----
- Sentiment is a simple rule-based placeholder for MVP.
- Cron and connector hooks are stubs; implement real fetchers per platform.
- Negative reviews auto-create a TODO activity.

# -*- coding: utf-8 -*-
{
    "name": "Review Management",
    "summary": "Manage and respond to reviews across products, services and listings",
    "version": "18.0.1.0.0",
    "author": "Your Company",
    "website": "https://example.com",
    "category": "Marketing/Reviews",
    "license": "LGPL-3",
    "depends": ["base", "mail", "web"],
    "data": [
        "security/review_groups.xml",
        "security/ir.model.access.csv",
        "data/review_sequences.xml",
        "data/review_cron.xml",
        "views/review_menu.xml",
        "views/review_listing_views.xml",
        "views/review_review_views.xml",
        "views/review_response_template_views.xml",
        "views/review_dashboard_views.xml",
        "report/review_reports.xml",
    ],
    "assets": {
        "web.assets_backend": [],
    },
    "application": True,
    "installable": True,
}

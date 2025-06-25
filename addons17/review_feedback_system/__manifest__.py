{
    "name": "Review and Feedback System",
    "version": "17.0.1.0.0",
    "category": "Website/Website",
    "summary": "Comprehensive review and feedback management system for websites",
    "description": """
Review and Feedback Integration System
=====================================

A comprehensive system for collecting, managing, and displaying customer reviews and feedback.

Key Features:
* User-friendly review submission forms
* Automatic data capture and storage
* Website review display with ratings
* Advanced admin dashboard for review management
* Real-time notification system
* Analytics and reporting capabilities
* Responsive design for all devices
* Security and compliance features

This module enables businesses to:
- Collect valuable customer feedback
- Build trust through transparent reviews
- Improve products and services based on feedback
- Enhance website credibility
- Track customer satisfaction trends
    """,
    "author": "Nana Gaisie",
    "website": "https://github.com/nanagaisie1/odoo",
    "depends": [
        "base",
        "website",
        "mail",
        "product",
        "sale",
        "portal",
        "website_sale",
    ],
    "data": [
        "security/review_security.xml",
        "security/ir.model.access.csv",
        "data/review_email_templates.xml",
        "data/review_cron_jobs.xml",
        "views/review_views.xml",
        "views/review_category_views.xml",
        "views/review_analytics_views.xml",
        "views/review_settings_views.xml",
        "views/website_review_templates.xml",
        "views/portal_review_templates.xml",
        "views/menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "review_feedback_system/static/src/css/review_backend.css",
            "review_feedback_system/static/src/js/review_dashboard.js",
        ],
        "web.assets_frontend": [
            "review_feedback_system/static/src/css/review_frontend.css",
            "review_feedback_system/static/src/js/review_frontend.js",
        ],
    },
    "demo": [
        "demo/review_demo.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}

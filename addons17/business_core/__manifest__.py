{
    "name": "Business Management",
    "version": "1.0.0",
    "author": "Nana Gaisie",
    "maintaner": "Nana Gaisie",
    "website": "https://github.com/nanagaisie1/odoo",
    "summary": "Core Business Management System",
    "description": """
Business Management System
========================
A comprehensive business management system that provides core functionality for managing:

Key Features
-----------
* Business Profile Management
* App Integration Management
* Business Products
* Business Preferences
* App Categories

This module serves as the foundation for business operations, allowing you to:
- Create and manage business profiles with logos and descriptions
- Integrate various business applications
- Manage business-specific products
- Configure business preferences
- Organize apps into categories
    """,
    "category": "Administration/Business",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/business_views.xml",
        "views/business_preference_views.xml",
        "views/business_product_views.xml",
        "views/app_views.xml",
        "views/app_category_views.xml",
        "views/menus.xml",
    ],
    "demo": [],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}  # type: ignore

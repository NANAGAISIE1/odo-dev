{
    "name": "Identity Management",
    "version": "1.0",
    "summary": "Advanced KYC Management System",
    "author": "Nana Gaisie",
    "maintaner": "Nana Gaisie",
    "website": "https://github.com/nanagaisie1/odoo",
    "description": """
Know Your Customer (KYC) Management System
========================================
A comprehensive system for managing customer identity verification and documentation.

Key Features
-----------
* Customer Identity Verification
* Document Management
* Verification Workflow
* Compliance Tracking

This module enables:
- Secure storage and management of customer identification documents
- Streamlined verification processes
- Compliance with regulatory requirements
- Document validation and approval workflows
    """,
    "category": "Administration/Tools",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/kyc_views.xml",
        "views/menus.xml",
    ],
    "demo": [],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}  # type: ignore

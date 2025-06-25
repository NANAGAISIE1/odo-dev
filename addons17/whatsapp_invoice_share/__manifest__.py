{
    "name": "WhatsApp Invoice Share",
    "version": "17.0.1.0.0",
    "category": "Accounting",
    "summary": "Share invoice PDFs via WhatsApp Web",
    "description": """
        This module adds WhatsApp sharing functionality to invoices.
        Features:
        - Share button on invoice form view
        - Opens WhatsApp Web with pre-filled message to share invoice PDF
        - Uses customer phone number from partner record
        - Icon for WhatsApp button
        - Button visible for customer invoices and refunds
    """,
    "author": "Nana Gaisie",
    "website": "https://github.com/nanagaisie1",
    "depends": ["account"],
    "data": [
        "views/account_move_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "LGPL-3",
}

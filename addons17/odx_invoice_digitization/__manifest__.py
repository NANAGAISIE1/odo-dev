# -*- coding: utf-8 -*-
{
    "name": "Invoice Digitization",
    "description": """OCR is a powerful tool that uses the magic of OCR to automatically extract key information from your invoices and documents, streamlining your accounts payable (AP) process.""",
    "summary": "OCR is a powerful tool that uses the magic of OCR to automatically extract key information from your invoices and documents, streamlining your accounts payable (AP) process.",
    "version": "17.0.1.0.0",
    "category": "Accounting/Accounting",
    "author": "Odox SoftHub LLP",
    "website": "http://www.odoxsofthub.com",
    "support": "support@odoxsofthub.com",
    "depends": ["account"],
    "data": [
        "views/account_move.xml",
        "views/res_config_settings.xml",
    ],
    "images": ["static/description/thumbnail.gif"],
    "license": "LGPL-3",
    "installable": True,
    "application": True,
    "auto_install": False,
}

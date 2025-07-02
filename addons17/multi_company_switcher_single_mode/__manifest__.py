{
    "name": "Multi-company Switcher Single Mode",
    "version": "17.0.1.0.0",
    "category": "Tools",
    "summary": "Module for switching company only in single mode",
    "author": "Opsway",
    "website": "https://opsway.com",
    "depends": [
        "base_setup",
    ],
    "images": ["static/description/banner.png"],
    "assets": {
        "web.assets_backend": [
            (
                "after",
                "web/static/src/webclient/company_service.js",
                "multi_company_switcher_single_mode/static/src/webclient/company_service.js",
            ),
            "multi_company_switcher_single_mode/static/src/webclient/switch_company_menu/switch_company_menu.js",
            "multi_company_switcher_single_mode/static/src/webclient/switch_company_menu/switch_company_menu.scss",
        ],
    },
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}  # type: ignore

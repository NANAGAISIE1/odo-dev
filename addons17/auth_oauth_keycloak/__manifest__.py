{
    "name": "Auth OAuth Keycloak",
    "summary": """
        Enables Keycloack integration for the OAuth2 Authentication module.
    """,
    "author": "Mint System",
    "website": "https://www.mint-system.ch",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "version": "17.0.1.0.0",
    "depends": [
        "base",
        "auth_oauth",
    ],
    "data": [
        "views/auth_oauth.xml",
    ],
    "images": ["images/screen.png"],
    "post_init_hook": "post_init_hook",
}  # type: ignore

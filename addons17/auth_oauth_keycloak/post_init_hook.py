def post_init_hook(env):
    """Post-install hook to ensure proper module initialization"""
    # Force update of the auth.oauth.provider model
    env["auth.oauth.provider"]._fields
    env.cr.commit()

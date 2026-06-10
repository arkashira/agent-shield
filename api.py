from flask_principal import identity_loaded, Identity

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    pass  # Placeholder for identity loading logic

def api_endpoint():
    from flask_principal import current_user
    user_name = current_user.identity.name  # Correctly access identity
    return f"Hello, {user_name}"
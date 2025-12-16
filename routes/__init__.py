# from flask import Blueprint
from flask import Blueprint

# Import individual blueprints
from .users import users_bp
from .accounts import accounts_bp
from .transactions import transactions_bp

# Optional: make them easily accessible when importing *
__all__ = ["users_bp", "accounts_bp", "transactions_bp"]

# Function to register all blueprints to the Flask app
def register_routes(app):
    app.register_blueprint(users_bp)        # Register /users routes
    app.register_blueprint(accounts_bp)     # Register /accounts routes
    app.register_blueprint(transactions_bp) # Register /transactions routes


# from .users import users_bp
# from .accounts import accounts_bp
# from .transactions import transactions_bp

# __all__ = ["users_bp", "accounts_bp", "transactions_bp"]


# def register_routes(app):
#     app.register_blueprint(users_bp)
#     app.register_blueprint(accounts_bp)
#     app.register_blueprint(transactions_bp)

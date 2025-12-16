# # ABORIGINAL BANK
# # REQUIREMENTS: A BANK APP THAT CAN MAKE A PROFILE. NAME, DOB, ADDRESS, ID, ACCOUNT INFO,BALANCE,JOB BOX, BEING ABLE TO EDIT INFORMATION  AND A RECEIVED RECEPTIY

# # STEP 1:
# # CREATE AN APP FLASK WITH CORRECT IMPORTS
# # CREATE AN API THAT BUILDS A DATABASE THAT TAKES IN NAME, DOB, ADDRESS, ID, ACCOUNT INFO,BALANCE,JOB BOX


from flask import Flask, jsonify, request            # Flask web framework, JSON responses, request data
from flask_sqlalchemy import SQLAlchemy              # SQLAlchemy ORM for database handling
from datetime import datetime                         # For timestamps in transactions, accounts, etc.
from config import Config                             # App configuration (DB URI, settings)
from models import db, User, Account, Transaction    # Import database and models
from routes import register_routes                    # Function to register all routes
from routes.auth import auth_bp                       # Auth blueprint for login/signup routes
from flask_jwt_extended import (                     # JWT for authentication
    create_access_token,                             # Generate access token
    create_refresh_token,                            # Generate refresh token
    jwt_required,                                    # Protect routes
    get_jwt_identity,                                # Get identity from token
    JWTManager                                       # JWT manager
)
from flask_cors import CORS


app = Flask(__name__)                                 # Create Flask application


CORS(app, origins=["https://bank-frontend-self.vercel.app"])
# Create database configuration
app.config.from_object(Config)                        # Load configuration from Config class
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"  # Override DB path for local SQLite

# Initialize database
db.init_app(app)                                      # Link SQLAlchemy with this Flask app

# Initialize JWT manager
jwt = JWTManager(app)                                 # Enable JWT authentication

# Register all routes
register_routes(app)                                  # Add routes from routes.py
app.register_blueprint(auth_bp)                       # Add auth routes (login, signup) via blueprint

# Optional test routes (commented out)
# @app.route("/")
# def home():
#     return jsonify({"MESSAGE": "SUCCESS, BANK API ONLINE"})
#
# @app.route("/<name>")
# def user(name):
#     return f"{name.capitalize()} PAGE!"
#
# @app.route("/account")
# def account():
#     return "ACCOUNT PAGE!"
#
# @app.route("/transaction")
# def transaction():
#     return "TRANSACTION PAGE!"

if __name__ == "__main__":                             # Only run if file executed directly
    with app.app_context():                            # Ensure app context for DB operations
        db.create_all()                                # Create all tables if they don't exist
    app.run(debug=True)                                # Start Flask app in debug mode


# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from config import Config
# from models import db, User, Account, Transaction
# from routes import register_routes
# from routes.auth import auth_bp
# from flask_jwt_extended import (
#     create_access_token,
#     create_refresh_token,
#     jwt_required,
#     get_jwt_identity,
#     JWTManager
# )
# app = Flask(__name__)
# # create db
# app.config.from_object(Config)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
# # initialize db
# db.init_app(app)

# # Init JWT manager
# jwt = JWTManager(app)
# # register all routes
# register_routes(app)
# app.register_blueprint(auth_bp)  # ensure auth routes are available
# # db.init_app(app)

# # @app.route("/")
# # def home():
# #     return jsonify({"MESSAGE": "SUCCESS, BANK API ONLINE"})


# # @app.route("/<name>")
# # def user(name):
# #     return f"{name.capitalize()} PAGE!"


# # @app.route("/account")
# # def account():
# #     return "ACCOUNT PAGE!"


# # @app.route("/transaction")
# # def transaction():
# #     return "TRANSACTION PAGE!"


# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()  # creates tables if they don't exist
#     app.run(debug=True)

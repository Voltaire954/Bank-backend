from flask import Blueprint, request, jsonify         # Blueprint for routes, request for input, jsonify for JSON output
from models import db
from models.user import User                           # Import User model
from flask_jwt_extended import (                      # JWT helpers
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from datetime import timedelta

# Blueprint for authentication routes, all start with /auth
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# ============================================================
# SIGNUP
# ============================================================
@auth_bp.post("/signup")                               # POST /auth/signup → create a new user
def signup():
    data = request.get_json() or {}                    # Get JSON data from request

    # Required fields
    required = ["username", "password", "name", "dob", "email"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Check for existing username or email
    if User.query.filter((User.username == data["username"]) | (User.email == data["email"])).first():
        return jsonify({"error": "Username or email already exists"}), 400

    # Create user object
    user = User(
        username=data["username"],
        name=data["name"],
        dob=data["dob"],                                # Expecting YYYY-MM-DD string
        email=data["email"],
        job=data.get("job")                             # Optional field
    )
    user.set_password(data["password"])                 # Hash password before storing

    db.session.add(user)                                # Add to DB session
    db.session.commit()                                 # Commit to database

    return jsonify({"message": "User created", "user": user.to_dict()}), 201

# ============================================================
# LOGIN
# ============================================================
@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    username_or_email = data.get("username")   # Frontend still sends 'username'
    password = data.get("password")

    if not username_or_email or not password:
        return jsonify({"error": "username/email and password required"}), 400

    # Allow login with either username OR email
    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }), 200

# ============================================================
# PROTECTED ROUTE: CURRENT USER
# ============================================================
@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()                       # Get user ID from JWT
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Add accounts and transactions to the response
    user_data = user.to_dict()
    user_data["accounts"] = [account.to_dict() for account in user.accounts]
    user_data["transactions"] = [txn.to_dict() for txn in user.transactions]

    return jsonify(user_data), 200


# # routes/auth.py
# from flask import Blueprint, request, jsonify
# from models import db
# from models.user import User
# from flask_jwt_extended import (
#     create_access_token,
#     create_refresh_token,
#     jwt_required,
#     get_jwt_identity,
#     JWTManager
# )
# from datetime import timedelta

# auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# # Signup
# @auth_bp.post("/signup")
# def signup():
#     data = request.get_json() or {}
#     required = ["username", "password", "name", "dob", "email"]
#     for field in required:
#         if field not in data:
#             return jsonify({"error": f"Missing field: {field}"}), 400

#     if User.query.filter((User.username == data["username"]) | (User.email == data["email"])).first():
#         return jsonify({"error": "Username or email already exists"}), 400

#     user = User(
#         username=data["username"],
#         name=data["name"],
#         dob=data["dob"],
#         email=data["email"],
#         job_box=data.get("job_box")
#     )
#     user.set_password(data["password"])

#     db.session.add(user)
#     db.session.commit()

#     return jsonify({"message": "User created", "user": user.to_dict()}), 201


# # Login
# @auth_bp.post("/login")
# def login():
#     data = request.get_json() or {}
#     username = data.get("username")
#     password = data.get("password")
#     if not username or not password:
#         return jsonify({"error": "username and password required"}), 400

#     user = User.query.filter_by(username=username).first()
#     if not user or not user.check_password(password):
#         return jsonify({"error": "Invalid credentials"}), 401

#     # Create tokens
#     access_token = create_access_token(identity=user.id)
#     refresh_token = create_refresh_token(identity=user.id)

#     return jsonify({
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "user": user.to_dict()
#     }), 200


# # Example protected route
# @auth_bp.get("/me")
# @jwt_required()
# def me():
#     user_id = get_jwt_identity()
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({"error": "User not found"}), 404
#     return jsonify(user.to_dict()), 200

from flask import Blueprint, jsonify, request          # Blueprint for routes, request for input, jsonify for JSON output
from models import db, User, Account                   # Import DB, User and Account models
from datetime import datetime                           # For timestamps

# Blueprint for accounts routes, all URLs start with /accounts
accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")

# ============================================================
# GET ALL ACCOUNTS
# ============================================================
@accounts_bp.get("/")                                  # GET /accounts → returns all accounts
def get_all_accounts():
    accounts = Account.query.all()
    return jsonify([
        {
            "id": a.id,
            "user_id": a.user_id,
            "balance": float(a.balance),
            "date_added": a.date_added
        } for a in accounts
    ])

# ============================================================
# GET ACCOUNT BY ID
# ============================================================
@accounts_bp.get("/<int:account_id>")                 # GET /accounts/<id> → single account
def get_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({
        "id": account.id,
        "user_id": account.user_id,
        "balance": float(account.balance),
        "date_added": account.date_added
    })

# ============================================================
# CREATE ACCOUNT
# ============================================================
@accounts_bp.post("/")                                 # POST /accounts → create a new account
def create_account():
    data = request.get_json()
    user_id = data.get("user_id")
    starting_balance = data.get("balance", 0.00)       # Default balance = 0

    # Validate user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User does not exist"}), 404

    # Optional: only one account per user
    if Account.query.filter_by(user_id=user.id).first():
        return jsonify({"error": "User already has an account"}), 400

    # Create account
    account = Account(
        user_id=user.id,
        balance=starting_balance,
        date_added=datetime.utcnow()
    )
    db.session.add(account)
    db.session.commit()

    return jsonify({
        "message": "Account created",
        "id": account.id,
        "user_id": user.id,
        "balance": float(account.balance)
    }), 201

# ============================================================
# UPDATE ACCOUNT
# ============================================================
@accounts_bp.put("/<int:account_id>")                 # PUT /accounts/<id> → update account (minimal here)
def update_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    data = request.get_json()
    # Only allow balance updates via transactions; other updates can go here
    db.session.commit()
    return jsonify({"message": "Account updated"})

# ============================================================
# DELETE ACCOUNT
# ============================================================
@accounts_bp.delete("/<int:account_id>")              # DELETE /accounts/<id> → delete account
def delete_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    # Prevent deletion if transactions exist
    if account.transactions:
        return jsonify({"error": "Cannot delete account with existing transactions"}), 400

    db.session.delete(account)
    db.session.commit()
    return jsonify({"message": "Account deleted"})


# from flask import Blueprint, jsonify, request
# from models import db, User, Account
# from datetime import datetime

# accounts_bp = Blueprint("accounts", __name__, url_prefix="/accounts")

# # --------------------------
# # GET ALL ACCOUNTS
# # --------------------------


# @accounts_bp.get("/")
# def get_all_accounts():
#     accounts = Account.query.all()
#     return jsonify([{
#         "id": a.id,
#         "user_id": a.user_id,
#         "balance": float(a.balance),
#         "date_added": a.date_added
#     } for a in accounts])

# # --------------------------
# # GET ACCOUNT BY ID
# # --------------------------


# @accounts_bp.get("/<int:account_id>")
# def get_account(account_id):
#     account = Account.query.get(account_id)
#     if not account:
#         return jsonify({"error": "Account not found"}), 404
#     return jsonify({
#         "id": account.id,
#         "user_id": account.user_id,
#         "balance": float(account.balance),
#         "date_added": account.date_added
#     })

# # --------------------------
# # CREATE ACCOUNT
# # --------------------------


# @accounts_bp.post("/")
# def create_account():
#     data = request.get_json()
#     user_id = data.get("user_id")
#     starting_balance = data.get("balance", 0.00)

#     # Validate user exists
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({"error": "User does not exist"}), 404

#     # Optional: only one account per user
#     if Account.query.filter_by(user_id=user.id).first():
#         return jsonify({"error": "User already has an account"}), 400

#     account = Account(
#         user_id=user.id,
#         balance=starting_balance,
#         date_added=datetime.utcnow()
#     )
#     db.session.add(account)
#     db.session.commit()

#     return jsonify({
#         "message": "Account created",
#         "id": account.id,
#         "user_id": user.id,
#         "balance": float(account.balance)
#     }), 201

# # --------------------------
# # UPDATE ACCOUNT
# # --------------------------


# @accounts_bp.put("/<int:account_id>")
# def update_account(account_id):
#     account = Account.query.get(account_id)
#     if not account:
#         return jsonify({"error": "Account not found"}), 404

#     data = request.get_json()
#     # Only allow balance updates via transactions, optional name updates here
#     db.session.commit()
#     return jsonify({"message": "Account updated"})

# # --------------------------
# # DELETE ACCOUNT
# # --------------------------


# @accounts_bp.delete("/<int:account_id>")
# def delete_account(account_id):
#     account = Account.query.get(account_id)
#     if not account:
#         return jsonify({"error": "Account not found"}), 404

#     if account.transactions:
#         return jsonify({"error": "Cannot delete account with existing transactions"}), 400

#     db.session.delete(account)
#     db.session.commit()
#     return jsonify({"message": "Account deleted"})

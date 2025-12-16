# Blueprint for routes, request for input, jsonify for JSON output
from flask import Blueprint, jsonify, request
# Import DB, Account, Transaction models
from models import db, Account, Transaction
from datetime import datetime                       # For timestamps
# Function to generate PDF receipts
from utils.pdf_generator import generate_pdf_receipt
import json
import os

# Blueprint for transactions routes, all start with /transactions
transactions_bp = Blueprint(
    "transactions", __name__, url_prefix="/transactions")

# ============================================================
# Helper: Log transaction into database
# ============================================================


def log_transaction(user_id, account_id, amount, txn_type):
    txn = Transaction(
        user_id=user_id,
        account_id=account_id,
        amount=amount,
        transaction_type=txn_type,
        date_added=datetime.utcnow()
    )
    db.session.add(txn)        # Add transaction to DB session
    return txn                  # Return txn object (not yet committed)

# ============================================================
# Helper: Save JSON + PDF receipts
# ============================================================


def generate_receipts(transaction):
    os.makedirs("receipts", exist_ok=True)  # Ensure receipts folder exists

    # JSON receipt
    json_receipt = {
        "receipt_id": f"tx-{transaction.id}",
        "transaction_id": transaction.id,
        "user_id": transaction.user_id,
        "account_id": transaction.account_id,
        "transaction_type": transaction.transaction_type,
        "amount": str(transaction.amount),
        "date": transaction.date_added.isoformat()
    }

    # Save JSON
    json_path = f"receipts/transaction_{transaction.id}.json"
    with open(json_path, "w") as f:
        json.dump(json_receipt, f, indent=4)

    # Generate PDF
    pdf_path = f"receipts/transaction_{transaction.id}.pdf"
    generate_pdf_receipt(transaction, pdf_path)

    return json_path, pdf_path, json_receipt

# ============================================================
# GET ALL TRANSACTIONS
# ============================================================


@transactions_bp.get("/")  # GET /transactions → all transactions
def get_all_transactions():
    txns = Transaction.query.all()
    return jsonify([
        {
            "id": t.id,
            "user_id": t.user_id,
            "account_id": t.account_id,
            "amount": float(t.amount),
            "transaction_type": t.transaction_type,
            "date_added": t.date_added
        } for t in txns
    ])

# ============================================================
# GET TRANSACTION BY ID
# ============================================================


@transactions_bp.get("/<int:txn_id>")  # GET /transactions/<id>
def get_transaction(txn_id):
    t = Transaction.query.get(txn_id)
    if not t:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify({
        "id": t.id,
        "user_id": t.user_id,
        "account_id": t.account_id,
        "amount": float(t.amount),
        "transaction_type": t.transaction_type,
        "date_added": t.date_added
    })

# ============================================================
# DEPOSIT
# ============================================================


@transactions_bp.post("/deposit")  # POST /transactions/deposit
def deposit():
    data = request.get_json() or {}

    account_id = data.get("account_id")
    amount = data.get("amount")

    if account_id is None or amount is None:
        return jsonify({"error": "account_id and amount are required"}), 400

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "amount must be a number"}), 400

    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400

    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    # Update balance
    account.balance = float(account.balance) + amount

    # Log transaction
    txn = log_transaction(account.user_id, account.id, amount, "deposit")
    db.session.commit()

    # Generate receipts
    json_path, pdf_path, json_receipt = generate_receipts(txn)

    return jsonify({
        "message": "Deposit successful",
        "new_balance": float(account.balance),
        "transaction": json_receipt,
        "receipt_json": json_path,
        "receipt_pdf": pdf_path
    }), 201

# ============================================================
# WITHDRAW
# ============================================================


@transactions_bp.post("/withdraw")  # POST /transactions/withdraw
def withdraw():
    data = request.get_json()
    account_id = data.get("account_id")
    amount = data.get("amount")

    if not account_id or not amount:
        return jsonify({"error": "account_id and amount required"}), 400

    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400

    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    if account.balance < amount:
        return jsonify({"error": "Insufficient funds"}), 400

    # Update balance
    account.balance -= amount

    # Log transaction
    txn = log_transaction(account.user_id, account.id, amount, "withdrawal")
    db.session.commit()

    # Generate receipts
    json_path, pdf_path, json_receipt = generate_receipts(txn)

    return jsonify({
        "message": "Withdrawal successful",
        "new_balance": float(account.balance),
        "transaction": json_receipt,
        "receipt_json": json_path,
        "receipt_pdf": pdf_path
    })

# ============================================================
# TRANSFER
# ============================================================


@transactions_bp.post("/transfer")  # POST /transactions/transfer
def transfer():
    data = request.get_json()

    from_id = data.get("from_account_id")
    to_id = data.get("to_account_id")
    amount = data.get("amount")

    if not all([from_id, to_id, amount]):
        return jsonify({"error": "from_account_id, to_account_id, amount required"}), 400

    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400

    from_acct = Account.query.get(from_id)
    to_acct = Account.query.get(to_id)

    if not from_acct or not to_acct:
        return jsonify({"error": "One or both accounts not found"}), 404

    if from_acct.balance < amount:
        return jsonify({"error": "Insufficient funds"}), 400

    # Update balances
    from_acct.balance -= amount
    to_acct.balance += amount

    # Log transactions
    out_txn = log_transaction(
        from_acct.user_id, from_acct.id, amount, "transfer_out")
    in_txn = log_transaction(
        to_acct.user_id, to_acct.id, amount, "transfer_in")
    db.session.commit()

    # Generate receipts
    out_json_path, out_pdf_path, out_json = generate_receipts(out_txn)
    in_json_path, in_pdf_path, in_json = generate_receipts(in_txn)

    return jsonify({
        "message": "Transfer successful",
        "from_account_balance": float(from_acct.balance),
        "to_account_balance": float(to_acct.balance),
        "receipts": {
            "outgoing": {"json": out_json_path, "pdf": out_pdf_path},
            "incoming": {"json": in_json_path, "pdf": in_pdf_path}
        }
    })


# from flask import Blueprint, jsonify, request
# from models import db, Account, Transaction
# from datetime import datetime
# from utils.pdf_generator import generate_pdf_receipt   # <--- clean import
# import json
# import os

# transactions_bp = Blueprint(
#     "transactions", __name__, url_prefix="/transactions"
# )

# # ============================================================
# # Helper: Log transaction into database
# # ============================================================
# def log_transaction(user_id, account_id, amount, txn_type):
#     txn = Transaction(
#         user_id=user_id,
#         account_id=account_id,
#         amount=amount,
#         transaction_type=txn_type,
#         date_added=datetime.utcnow()
#     )
#     db.session.add(txn)
#     return txn


# # ============================================================
# # Helper: Save JSON + PDF receipts
# # ============================================================
# def generate_receipts(transaction):
#     os.makedirs("receipts", exist_ok=True)

#     json_receipt = {
#         "receipt_id": f"tx-{transaction.id}",
#         "transaction_id": transaction.id,
#         "user_id": transaction.user_id,
#         "account_id": transaction.account_id,
#         "transaction_type": transaction.transaction_type,
#         "amount": str(transaction.amount),
#         "date": transaction.date_added.isoformat()
#     }

#     # JSON PATH
#     json_path = f"receipts/transaction_{transaction.id}.json"
#     with open(json_path, "w") as f:
#         json.dump(json_receipt, f, indent=4)

#     # PDF PATH
#     pdf_path = f"receipts/transaction_{transaction.id}.pdf"
#     generate_pdf_receipt(transaction, pdf_path)

#     return json_path, pdf_path, json_receipt


# # ============================================================
# # GET ALL TRANSACTIONS
# # ============================================================
# @transactions_bp.get("/")
# def get_all_transactions():
#     txns = Transaction.query.all()
#     return jsonify([
#         {
#             "id": t.id,
#             "user_id": t.user_id,
#             "account_id": t.account_id,
#             "amount": float(t.amount),
#             "transaction_type": t.transaction_type,
#             "date_added": t.date_added
#         } for t in txns
#     ])


# # ============================================================
# # GET TRANSACTION BY ID
# # ============================================================
# @transactions_bp.get("/<int:txn_id>")
# def get_transaction(txn_id):
#     t = Transaction.query.get(txn_id)
#     if not t:
#         return jsonify({"error": "Transaction not found"}), 404

#     return jsonify({
#         "id": t.id,
#         "user_id": t.user_id,
#         "account_id": t.account_id,
#         "amount": float(t.amount),
#         "transaction_type": t.transaction_type,
#         "date_added": t.date_added
#     })


# # ============================================================
# # DEPOSIT
# # ============================================================
# @transactions_bp.post("/deposit")
# def deposit():
#     data = request.get_json() or {}

#     # Validate required fields
#     account_id = data.get("account_id")
#     amount = data.get("amount")

#     if account_id is None or amount is None:
#         return jsonify({"error": "account_id and amount are required"}), 400

#     # Ensure amount is numeric
#     try:
#         amount = float(amount)
#     except ValueError:
#         return jsonify({"error": "amount must be a number"}), 400

#     # Validate positive amount
#     if amount <= 0:
#         return jsonify({"error": "Amount must be positive"}), 400

#     # Fetch account
#     account = Account.query.get(account_id)
#     if not account:
#         return jsonify({"error": "Account not found"}), 404

#     # Perform deposit
#     account.balance = float(account.balance) + amount

#     # Log transaction
#     txn = log_transaction(
#         user_id=account.user_id,
#         account_id=account.id,
#         amount=amount,
#         txn_type="deposit"
#     )

#     db.session.commit()

#     # Generate receipts
#     json_path, pdf_path, json_receipt = generate_receipts(txn)

#     return jsonify({
#         "message": "Deposit successful",
#         "new_balance": float(account.balance),
#         "transaction": json_receipt,
#         "receipt_json": json_path,
#         "receipt_pdf": pdf_path
#     }), 201

# # ============================================================
# # WITHDRAW
# # ============================================================
# @transactions_bp.post("/withdraw")
# def withdraw():
#     data = request.get_json()
#     account_id = data.get("account_id")
#     amount = data.get("amount")

#     if not account_id or not amount:
#         return jsonify({"error": "account_id and amount required"}), 400

#     if amount <= 0:
#         return jsonify({"error": "Amount must be positive"}), 400

#     account = Account.query.get(account_id)
#     if not account:
#         return jsonify({"error": "Account not found"}), 404

#     if account.balance < amount:
#         return jsonify({"error": "Insufficient funds"}), 400

#     # Perform withdrawal
#     account.balance -= amount

#     # Log transaction
#     txn = log_transaction(
#         user_id=account.user_id,
#         account_id=account.id,
#         amount=amount,
#         txn_type="withdrawal"
#     )

#     db.session.commit()

#     # Receipts
#     json_path, pdf_path, json_receipt = generate_receipts(txn)

#     return jsonify({
#         "message": "Withdrawal successful",
#         "new_balance": float(account.balance),
#         "receipt_pdf": pdf_path,
#         "receipt_json": json_path,
#         "transaction": json_receipt
#     })


# # ============================================================
# # TRANSFER
# # ============================================================
# @transactions_bp.post("/transfer")
# def transfer():
#     data = request.get_json()

#     from_id = data.get("from_account_id")
#     to_id = data.get("to_account_id")
#     amount = data.get("amount")

#     if not all([from_id, to_id, amount]):
#         return jsonify({"error": "from_account_id, to_account_id, amount required"}), 400

#     if amount <= 0:
#         return jsonify({"error": "Amount must be positive"}), 400

#     from_acct = Account.query.get(from_id)
#     to_acct = Account.query.get(to_id)

#     if not from_acct or not to_acct:
#         return jsonify({"error": "One or both accounts not found"}), 404

#     if from_acct.balance < amount:
#         return jsonify({"error": "Insufficient funds"}), 400

#     # Update balances
#     from_acct.balance -= amount
#     to_acct.balance += amount

#     # Log outgoing transaction
#     out_txn = log_transaction(
#         user_id=from_acct.user_id,
#         account_id=from_acct.id,
#         amount=amount,
#         txn_type="transfer_out"
#     )

#     # Log incoming transaction
#     in_txn = log_transaction(
#         user_id=to_acct.user_id,
#         account_id=to_acct.id,
#         amount=amount,
#         txn_type="transfer_in"
#     )

#     db.session.commit()

#     # Receipts for both
#     out_json_path, out_pdf_path, out_json = generate_receipts(out_txn)
#     in_json_path, in_pdf_path, in_json = generate_receipts(in_txn)

#     return jsonify({
#         "message": "Transfer successful",
#         "from_account_balance": float(from_acct.balance),
#         "to_account_balance": float(to_acct.balance),
#         "receipts": {
#             "outgoing": {"json": out_json_path, "pdf": out_pdf_path},
#             "incoming": {"json": in_json_path, "pdf": in_pdf_path}
#         }
#     })

# For any OS/path utilities (not strictly needed here)
import os
# For timestamps like date_added
from datetime import datetime
# Import SQLAlchemy instance from package
from . import db


class Transaction(db.Model):                      # Transaction table
    __tablename__ = 'transactions'               # Table name in DB

    id = db.Column(db.Integer, primary_key=True)  # Unique transaction ID
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # Link to the User who made the transaction

    account_id = db.Column(db.Integer, db.ForeignKey(
        "accounts.id"), nullable=False)
    # Link to the Account involved in the transaction

    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    # Transaction amount (supports decimals, max 10 digits, 2 after decimal)

    transaction_type = db.Column(db.String, nullable=False)
    # Type of transaction: "deposit", "withdrawal", or "transfer"

    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Timestamp when transaction was created


# import os
# from datetime import datetime
# from . import db


# class Transaction(db.Model):
#     __tablename__ = 'transactions'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#     account_id = db.Column(db.Integer, db.ForeignKey(
#         "accounts.id"), nullable=False)
#     amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
#     # "deposit", "withdrawal", "transfer"
#     transaction_type = db.Column(db.String, nullable=False)
#     date_added = db.Column(db.DateTime, default=datetime.utcnow)

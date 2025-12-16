import os                                         # For OS/path utilities (not strictly needed here)
from datetime import datetime                     # For timestamps like date_added
from . import db                                  # Import SQLAlchemy instance from package

class Account(db.Model):                          # Account table
    __tablename__ = 'accounts'                    # Table name in DB

    id = db.Column(db.Integer, primary_key=True)  # Unique account ID
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # Link to the User who owns this account

    account_type = db.Column(db.String, default="checking")
    # Optional: "checking", "savings", etc. Default is "checking"

    balance = db.Column(db.Numeric(precision=10, scale=2), default=0)
    # Account balance (supports decimals, max 10 digits, 2 after decimal)

    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Timestamp when account was created

    # Relationships
    transactions = db.relationship("Transaction", backref="account", lazy=True)
    # Link to all transactions for this account

    # Methods
    def adjust_balance(self, amount):             # Adjust balance (deposit or withdrawal)
        self.balance += amount
        if self.balance < 0:                      # Raise error if insufficient funds
            raise ValueError("Insufficient funds")


# import os
# from datetime import datetime
# from . import db


# class Account(db.Model):
#     __tablename__ = 'accounts'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
#     # optional: checking/savings
#     account_type = db.Column(db.String, default="checking")
#     balance = db.Column(db.Numeric(precision=10, scale=2), default=0)
#     date_added = db.Column(db.DateTime, default=datetime.utcnow)

#     def adjust_balance(self, amount):
#         self.balance += amount
#         if self.balance < 0:
#             raise ValueError("Insufficient funds")

#     # relationship
#     transactions = db.relationship(
#         "Transaction", backref="account", lazy=True,)

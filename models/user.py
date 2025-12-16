import os                                         # For any OS/path utilities
from datetime import datetime                     # For timestamps like date_added
from . import db                                  # Import SQLAlchemy instance from package
from werkzeug.security import generate_password_hash, check_password_hash  # Password hashing utilities

class User(db.Model):                             # User table
    __tablename__ = 'users'                       # Table name in DB

    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    username = db.Column(db.String, nullable=False, unique=True)  # Username (required, unique)
    name = db.Column(db.String, nullable=False)   # Full name
    dob = db.Column(db.Date, nullable=False)      # Date of birth
    email = db.Column(db.String, nullable=False, unique=True)    # Email (required, unique)
    job = db.Column(db.String, nullable=True)     # Optional job field
    date_added = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for creation

    password_hash = db.Column(db.String, nullable=False)  # Store hashed password

    # Relationships
    accounts = db.relationship("Account", backref="user", lazy=True)         # User → multiple accounts
    transactions = db.relationship("Transaction", backref="user", lazy=True) # User → multiple transactions

    def set_password(self, password: str):        # Hash and store password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:  # Check password against stored hash
        return check_password_hash(self.password_hash, password)

    def to_dict(self):                             # Return safe dict representation for API
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "dob": self.dob.isoformat() if self.dob else None,
            "email": self.email,
            "job": self.job,
            "date_added": self.date_added.isoformat() if self.date_added else None
        }


# import os
# from datetime import datetime
# from . import db
# from werkzeug.security import generate_password_hash, check_password_hash

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, nullable=False, unique=True)
#     name = db.Column(db.String, nullable=False)
#     dob = db.Column(db.Date, nullable=False)
#     # address = db.Column(db.String, nullable=True)
#     email = db.Column(db.String, nullable=False, unique=True)
#     job = db.Column(db.String, nullable=True)
#     date_added = db.Column(db.DateTime, default=datetime.utcnow)

#     def set_password(self,password:str):
#          #"""Hash and set the user's password."""
#         self.password_hash = generate_password_hash(password)
#     def check_password(self, password: str) -> bool:
#         """Return True if password matches stored hash."""
#         return check_password_hash(self.password_hash, password)

#     def to_dict(self):
#         """Return a safe dict representation (omit password)."""
#         return {
#             "id": self.id,
#             "username": self.username,
#             "name": self.name,
#             "dob": self.dob,
#             "email": self.email,
#             "job_box": self.job,
#             "date_added": self.date_added.isoformat() if self.date_added else None
#         }

accounts = db.relationship("Account", backref="user", lazy=True)
transactions = db.relationship("Transaction", backref="user", lazy=True)

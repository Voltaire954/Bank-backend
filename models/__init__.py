from flask_sqlalchemy import SQLAlchemy            # Import SQLAlchemy ORM

db = SQLAlchemy()                                  # Create the database instance to use across models

# Import models so SQLAlchemy knows about them
from .user import User                              # User model (users table)
from .account import Account                        # Account model (accounts table)
from .transaction import Transaction                # Transaction model (transactions table)


# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# from .user import User
# from .account import Account
# from .transaction import Transaction

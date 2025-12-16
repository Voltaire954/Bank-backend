from datetime import date                        # For setting birth dates
from app import app                               # Import Flask app
from models import db, User, Account, Transaction  # Import models
from config import Config





def seed_database():
    # Use app context to interact with the database
    with app.app_context():
        print("Resetting database...")

        # Drop all tables if they exist and recreate them
        db.drop_all()
        db.create_all()

        # --------------------------
        # Seed Users
        # --------------------------
        print("Seeding users...")
        user1 = User(
            username="jdoe",
            name="John Doe",
            dob=date(1990, 5, 12),
            email="jdoe@example.com",
            job="Engineer"
        )
        user1.set_password("password123")
        user2 = User(
            username="asmith",
            name="Alice Smith",
            dob=date(1985, 8, 23),
            email="asmith@example.com",
            job="Designer"
        )
        user2.set_password("password132")

        db.session.add_all([user1, user2])
        db.session.commit()  # Save users to database

        # --------------------------
        # Seed Accounts
        # --------------------------
        print("Seeding accounts...")
        acc1 = Account(user_id=user1.id,
                       account_type="checking", balance=1000.00)
        acc2 = Account(user_id=user1.id,
                       account_type="savings", balance=5000.00)
        acc3 = Account(user_id=user2.id,
                       account_type="checking", balance=2000.00)

        db.session.add_all([acc1, acc2, acc3])
        db.session.commit()  # Save accounts to database

        # --------------------------
        # Seed Transactions
        # --------------------------
        print("Seeding transactions...")
        tx1 = Transaction(user_id=user1.id, account_id=acc1.id,
                          amount=1000.00, transaction_type="deposit")
        tx2 = Transaction(user_id=user1.id, account_id=acc2.id,
                          amount=5000.00, transaction_type="deposit")
        tx3 = Transaction(user_id=user2.id, account_id=acc3.id,
                          amount=2000.00, transaction_type="deposit")
        tx4 = Transaction(user_id=user1.id, account_id=acc1.id,
                          amount=200.00, transaction_type="withdrawal")

        db.session.add_all([tx1, tx2, tx3, tx4])
        db.session.commit()  # Save transactions to database

        print("Seeding complete!")


# Run this script directly to seed the database
if __name__ == "__main__":
    seed_database()

# from datetime import date
# from app import app
# from models import db, User, Account, Transaction

# def seed_database():
#     with app.app_context():
#         print("Resetting database...")
#         db.drop_all()
#         db.create_all()

#         print("Seeding users...")
#         user1 = User(username="jdoe", name="John Doe", dob=date(1990, 5, 12), email="jdoe@example.com", job="Engineer")
#         user2 = User(username="asmith", name="Alice Smith", dob=date(1985, 8, 23), email="asmith@example.com", job="Designer")
#         db.session.add_all([user1, user2])
#         db.session.commit()

#         print("Seeding accounts...")
#         acc1 = Account(user_id=user1.id, account_type="checking", balance=1000.00)
#         acc2 = Account(user_id=user1.id, account_type="savings", balance=5000.00)
#         acc3 = Account(user_id=user2.id, account_type="checking", balance=2000.00)
#         db.session.add_all([acc1, acc2, acc3])
#         db.session.commit()

#         print("Seeding transactions...")
#         tx1 = Transaction(user_id=user1.id, account_id=acc1.id, amount=1000.00, transaction_type="deposit")
#         tx2 = Transaction(user_id=user1.id, account_id=acc2.id, amount=5000.00, transaction_type="deposit")
#         tx3 = Transaction(user_id=user2.id, account_id=acc3.id, amount=2000.00, transaction_type="deposit")
#         tx4 = Transaction(user_id=user1.id, account_id=acc1.id, amount=200.00, transaction_type="withdrawal")
#         db.session.add_all([tx1, tx2, tx3, tx4])
#         db.session.commit()

#         print("Seeding complete!")

# if __name__ == "__main__":
#     seed_database()

import os

class Config:
    # Use Postgres in production, fallback to SQLite locally
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///bank.db"  # fallback for local dev
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT settings
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")  # Secret key
    JWT_ACCESS_TOKEN_EXPIRES = 3600

# class Config:
#     DEBUG = True
    # Later, you can add database config
    # SQLALCHEMY_DATABASE_URI = "sqlite:///bank.db"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

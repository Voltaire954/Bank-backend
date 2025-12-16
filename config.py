# config.py
import os

class Config:
    # Production: Postgres, fallback: SQLite locally
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///user.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "supersecret"
    JWT_ACCESS_TOKEN_EXPIRES = 3600


# class Config:
#     DEBUG = True
    # Later, you can add database config
    # SQLALCHEMY_DATABASE_URI = "sqlite:///bank.db"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

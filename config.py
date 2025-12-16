import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "bank.db")

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT settings
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")  # Secret key
    JWT_ACCESS_TOKEN_EXPIRES = 3600

# class Config:
#     DEBUG = True
    # Later, you can add database config
    # SQLALCHEMY_DATABASE_URI = "sqlite:///bank.db"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

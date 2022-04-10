import os

# General
DEBUG = True

# Auth
SECRET_KEY = os.environ["LOFTAPI_SECRET_KEY"]

# Database
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

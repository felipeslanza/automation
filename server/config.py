import os

# General
DEBUG = True

# Auth
SECRET_KEY = os.environ.get("LOFTAPI_SECRET_KEY", "testkey")

# Database
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Pokemon service
POKEMON_ALLOWED_STARTING_TYPES = ("fire", "grass", "water")

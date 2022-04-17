import os

# General
DEBUG = True
LOGGING_LEVEL = "INFO"
LOGGING_FILEPATH = "server/out.log"  # set to empty to disable
LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(module)s - %(message)s"

# Auth
SECRET_KEY = os.environ.get("LOFTapp_SECRET_KEY", "testkey")

# Database
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Pokemon service
POKEMON_ALLOWED_STARTING_TYPES = ("fire", "grass", "water")
POKEMON_SCREENING_CACHE_FILEPATH = "server/pokemon_screening.cache"

import os

# General
DEBUG = True
LOGGING_LEVEL = "INFO"
LOGGING_FILEPATH = "server/out.log"  # set to empty to disable
LOGGING_FORMAT = f"%(asctime)s - %(levelname)s - %(module)s - %(message)s"

# Flask-specific
JSON_SORT_KEYS = False  # Must be `False` to allow relying on starting types order

# Auth
SECRET_KEY = os.environ.get("LOFTAPI_SECRET_KEY", "supersafekey")

# Database
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Pokemon service
POKEMON_ALLOWED_STARTING_TYPES = ("fire", "grass", "water")
POKEMON_SCREENING_CACHE_FILEPATH = "server/pokemon_screening.cache"

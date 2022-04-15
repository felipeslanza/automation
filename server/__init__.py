import logging
import os

from flask import Flask

from . import config


__all__ = ("api", "logger")


# +++++++++
# App setup
# +++++++++
api = Flask(__name__)
api.config.from_object(config)
logger = api.logger


# ++++++++++++
# Logger setup
# ++++++++++++
if config.LOGGING_FILEPATH:
    file_handler = logging.FileHandler(config.LOGGING_FILEPATH)
    file_handler.setFormatter(config.LOGGING_FORMAT)
    logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(config.LOGGING_FORMAT)
logger.addHandler(stream_handler)

logging_level = os.environ.get("LOGGING_LEVEL", config.LOGGING_LEVEL)
logger.setLevel(logging_level)

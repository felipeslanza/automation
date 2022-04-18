import logging
import os

from flask import Flask

from . import config


__all__ = ("app", "logger")


# +++++++++
# App setup
# +++++++++
app = Flask(__name__, static_folder="../client", static_url_path="/")
app.config.from_object(config)
logger = app.logger


# ++++++++++++
# Logger setup
# ++++++++++++
format_ = logging.Formatter(config.LOGGING_FORMAT)
if config.LOGGING_FILEPATH:
    file_handler = logging.FileHandler(config.LOGGING_FILEPATH)
    file_handler.setFormatter(format_)
    logger.addHandler(file_handler)

    # Add file handler to `werkzeug`
    logging.getLogger("werkzeug").addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(format_)
logger.addHandler(stream_handler)

logging_level = os.environ.get("LOGGING_LEVEL", config.LOGGING_LEVEL)
logger.setLevel(logging_level)

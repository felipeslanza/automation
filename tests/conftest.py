import pytest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


@pytest.fixture(scope="session")
def init_test_app():
    app = Flask("test_app")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://test/test_db.sqlite"
    app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db = SQLAlchemy()
    db.create_all()

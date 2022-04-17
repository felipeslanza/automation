import pytest

from server.app import app
from server.models import db


@pytest.fixture(scope="session")
def setup():
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SQLALCHEMY_COMMIT_ON_TEARDOWN": False,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    with app.app_context():
        db.init_app(app)


@pytest.fixture(scope="module")
def client(setup):
    with app.app_context():
        db.create_all()

        client_ = app.test_client()
        client_.db = db  # attaching `db` context for convenience

        yield client_

        db.drop_all()

import pytest

from server.api import api
from server.models import db


@pytest.fixture(scope="session")
def setup():
    api.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SQLALCHEMY_COMMIT_ON_TEARDOWN": False,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    with api.app_context():
        db.init_app(api)


@pytest.fixture(scope="module")
def client(setup):
    with api.app_context():
        db.create_all()

        client_ = api.test_client()
        client_.db = db  # attaching `db` context for convenience

        yield client_

        db.drop_all()

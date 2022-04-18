import pytest

from server.models import Trainer


@pytest.fixture(scope="module")
def trainer(client):
    trainer_ = Trainer(
        name="Jon",
        email="j@j.com",
        password="abcXYZ",
        birthday="1990-01-01",
    )

    db = client.db
    db.session.add(trainer_)
    db.session.commit()

    return trainer_


@pytest.fixture
def logged_trainer(trainer):
    trainer.token = trainer.generate_token()
    return trainer


def test_expired_token(client, trainer):
    token = trainer.generate_token(-5)  # expired
    res = client.get(
        "/api/trainer",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 401


def test_protected_routes_raise_401(client):
    s1 = client.get("/api/trainer").status_code
    s2 = client.put(
        "/api/trainer",
        json={"foo": "bar"},
        headers={"Authorization": "Bearer bad-token"},
    ).status_code
    s3 = client.delete("/api/trainer").status_code

    assert s1 == s2 == s3 == 401


def test_successful_token_attempt(client, logged_trainer):
    res = client.post(
        "/api/login", json=dict(email=logged_trainer.email, password="abcXYZ")
    )
    assert "token" in res.json


def test_failed_token_attempt(client, logged_trainer):
    res = client.post(
        "/api/login", json=dict(email=logged_trainer.email, password="hacker")
    )
    assert res.status_code == 401

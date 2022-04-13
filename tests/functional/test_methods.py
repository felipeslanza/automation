import pytest

from server.models import Trainer


@pytest.fixture
def post_trainer_data(client):
    return dict(name="Jon", email="j@j.com", password="123", birthday="1990-01-01")


def test_non_json_payload_raises(client, post_trainer_data):
    res = client.post("/trainer", data=post_trainer_data)
    assert res.status_code == 400


def test_trainer_creation(client, post_trainer_data):
    trainer = Trainer.query.filter_by(email=post_trainer_data["email"]).first()
    assert trainer is None

    res = client.post("/trainer", json=post_trainer_data)
    assert res.status_code == 201
    trainer = Trainer.query.filter_by(email=post_trainer_data["email"]).first()
    assert trainer

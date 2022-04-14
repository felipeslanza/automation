import pytest

from server.models import Trainer


@pytest.fixture
def post_trainer_data(client):
    return dict(name="Jon", email="j@j.com", password="123", birthday="1990-01-01")


@pytest.fixture
def logged_trainer(client, post_trainer_data):
    trainer = Trainer.query.get(1)
    trainer.token = trainer.generate_token()
    return trainer


def test_non_json_payload_raises(client, post_trainer_data):
    res = client.post("/api/trainer", data=post_trainer_data)
    assert res.status_code == 400


def test_new_trainer_post(client, post_trainer_data):
    trainer = Trainer.query.filter_by(email=post_trainer_data["email"]).first()
    assert trainer is None

    # Creation success
    res = client.post("/api/trainer", json=post_trainer_data)
    assert res.status_code == 201

    # Check `trainer` in `db`
    trainer = Trainer.query.filter_by(email=post_trainer_data["email"]).first()
    assert trainer

    # Check duplicate
    res = client.post("/api/trainer", json=post_trainer_data)
    assert res.status_code == 400
    assert "Existing trainer" in res.text


def test_handle_trainer_get_method(client, logged_trainer):
    res = client.get(
        f"/api/trainer/{logged_trainer.id}",
        headers={"Authorization": f"Bearer {logged_trainer.token}"},
    )

    assert res.status_code == 200
    assert res.json["email"] == logged_trainer.email


def test_handle_trainer_put_method(client, logged_trainer):
    pre = logged_trainer.email
    res = client.put(
        f"/api/trainer/{logged_trainer.id}",
        json=dict(email="x@x.co"),
        headers={"Authorization": f"Bearer {logged_trainer.token}"},
    )

    assert res.status_code == 200
    assert pre != logged_trainer.email


def test_handle_trainer_del_method(client, logged_trainer):
    res = client.delete(
        f"/api/trainer/{logged_trainer.id}",
        headers={"Authorization": f"Bearer {logged_trainer.token}"},
    )
    assert res.status_code == 200

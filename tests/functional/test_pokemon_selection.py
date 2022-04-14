import json

import pytest

from server.models import Trainer


@pytest.fixture(scope="module")
def logged_trainer(client):
    trainer_ = Trainer(
        name="Jon",
        email="j@j.com",
        password="abcXYZ",
        birthday="1990-01-01",
    )

    db = client.db
    db.session.add(trainer_)
    db.session.commit()

    trainer_.token = trainer_.generate_token()

    return trainer_


def test_pokemon_rotation(client, logged_trainer):
    assert logged_trainer.last_rotation is None

    res = client.get(
        "/api/initials-pokemon",
        headers={"Authorization": f"Bearer {logged_trainer.token}"},
    )

    assert res.status_code == 200
    assert logged_trainer.last_rotation


def test_selection_outside_rotation_fails(client, logged_trainer):
    obj = json.loads(logged_trainer.last_rotation)
    invalid_id = int(list(obj)[0]) + 1
    res = client.post(
        "/api/initials-pokemon/choose",
        json={"selected_species_id": invalid_id},
        headers={"Authorization": f"Bearer {logged_trainer.token}"},
    )

    assert res.status_code == 400
    assert trainer.pokemon is None


def test_selection_within_rotation_succeeds(client, logged_trainer):
    obj = json.loads(logged_trainer.last_rotation)
    valid_id = int(list(obj)[0])
    res = client.post(
        "/api/initials-pokemon/choose",
        json={"selected_species_id": valid_id},
        headers={"Authorization": f"Bearer {logged_trainer.token}"},
    )

    assert res.status_code == 200
    assert trainer.pokemon

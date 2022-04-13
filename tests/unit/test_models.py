import pytest

from server.models import Trainer, Pokemon


@pytest.fixture
def trainer():
    return Trainer(
        name="John",
        email="foo@bar.com",
        password="supersafe",
        birthday="1990-06-15",
    )


def test_new_trainer(client, trainer):
    assert trainer.name == "John"
    assert trainer.email == "foo@bar.com"
    assert trainer.password != "supersafe"
    assert trainer.birthday is not None
    assert trainer.id is None

    db = client.db
    db.session.add(trainer)
    db.session.commit()

    assert trainer.id


def test_trainer_password_not_in_obj(trainer):
    assert "password" not in trainer.as_dict()


def test_new_pokemon(client):
    pokemon = Pokemon(name="Charmander", species_id="XXX")
    assert pokemon.name == "Charmander"
    assert pokemon.id is None

    db = client.db
    db.session.add(pokemon)
    db.session.commit()

    assert pokemon.id

import pytest

from server.models import Trainer, Pokemon


def test_new_trainer():
    trainer = Trainer(
        name="John", email="foo@bar.com", password="supersafe", birthday="1990-06-15"
    )
    assert trainer.name == "John"
    assert trainer.email == "foo@bar.com"
    assert trainer.password != "supersafe"
    assert trainer.birthday is not None
    # assert trainer.id is not None


def test_new_pokemon():
    pokemon = Pokemon(name="Charmander")
    assert pokemon.name == "Charmander"

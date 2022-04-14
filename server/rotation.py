from typing import Union
import logging
import random

import pokebase as pb


_all__ = ("get_first_evolutions_by_type", "get_random_rotation")


logger = logging.getLogger(__name__)


def get_first_evolutions_by_type(type_: str) -> list:
    """Get all available pokemons by a single type

    ...

    Parameters
    ----------
    type_ : str
        strings with valid pokemon types
    """

    # +++++++++++++++++++++++++++++++++
    # TODO: add a persistent cache here
    # TODO: add a persistent cache here
    # TODO: add a persistent cache here
    # +++++++++++++++++++++++++++++++++

    try:
        meta = pb.type_(type_).pokemon
    except AttributeError:
        logger.error(f"Pokemon type {type_} not found!")
    else:
        return [i.pokemon for i in meta if i.pokemon.species.evolves_from_species is None]


def get_random_rotation(types: Union[str, list[str]]) -> list:
    """Randomly select one first-evolution pokemon for each provided `type`

    ...

    Parameters
    ----------
    types : str or list
        list of valid pokemon types
    """
    choices = []
    for type_ in types:
        first_evol = get_first_evolutions_by_type(type_)
        if first_evol:
            choices.append(random.choice(first_evol))

    return choices

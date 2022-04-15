from typing import Union
import logging
import random
import shelve

import pokebase as pb

from . import logger
from .config import POKEMON_ALLOWED_STARTING_TYPES, POKEMON_SCREENING_CACHE_FILEPATH


_all__ = ("get_first_evolutions_by_type", "get_random_rotation", "pre_build_cache")


def get_first_evolutions_by_type(
    type_: str,
    disable_cache: bool = False,
    shelve_flag: str = "r",
) -> dict:
    """Get all available pokemons by a single type

    ...

    Parameters
    ----------
    type_ : str
        strings with valid pokemon types
    """

    with shelve.open(POKEMON_SCREENING_CACHE_FILEPATH, flag=shelve_flag) as db:
        try:
            if disable_cache:
                raise KeyError
            obj = db[type_]
            logger.debug(f"Using cached results for type [{type_}]")
        except KeyError:
            logger.error(f"No cache found for type [{type_}], querying Pokeapi.")
            try:
                meta = pb.type_(type_).pokemon
            except AttributeError:
                logger.error(f"Pokemon type {type_} not found!")
                obj = {}
            else:
                eligible = filter(
                    lambda pokemon: pokemon.species.evolves_from_species is None,
                    map(lambda meta_: meta_.pokemon, meta),
                )
                obj = {p.id: p.name for p in eligible}

            db[type_] = obj

    return obj


def get_random_rotation(types: Union[str, list[str]]) -> dict:
    """Randomly select one first-evolution pokemon for each provided `type`

    ...

    Parameters
    ----------
    types : str or list
        list of valid pokemon types
    """
    choices = {}
    for type_ in types:
        pokemons_obj = get_first_evolutions_by_type(type_)
        if pokemons_obj:
            id_ = random.choice(list(pokemons_obj))
            choices[id_] = pokemons_obj[id_]

    return choices


def pre_build_cache():
    """Util to be called at server start to ensure cache is pre-generated,
    i.e. no write access is needed at run time.
    """
    for type_ in POKEMON_ALLOWED_STARTING_TYPES:
        _ = get_first_evolutions_by_type(type_, shelve_flag="c")

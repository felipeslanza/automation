from datetime import date
from typing import Optional
import logging


__all__ = "is_trainer_age_valid"


def is_trainer_age_valid(birthday: date, thresh: int = 14 * 365) -> bool:
    """Util to check if trainer age is greater than 14-years-old

    ...

    Parameters
    ----------
    birthday : date
        trainer's birthday as stored in the database
    """
    return (date.today() - birthday).days > thresh

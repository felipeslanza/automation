from datetime import datetime


__all__ = ("is_trainer_age_valid",)


def is_trainer_age_valid(birthday: datetime) -> bool:
    """Util to check if trainer age is greater than 14-years-old

    ...

    Parameters
    ----------
    birthday : datetime
        trainer's birthday as stored in database
    """
    return (datetime.today() - birthday).days > 14 * 365

from typing import Optional

from flask_httpauth import HTTPTokenAuth

from .models import Trainer


__all__ = ("auth",)


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token: str) -> Optional[Trainer]:
    return Trainer.verify_token(token)

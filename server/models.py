from __future__ import annotations
from typing import Optional
import logging
import time

from flask_sqlalchemy import SQLAlchemy
import jwt

from .config import SECRET_KEY


__all__ = ("Trainer", "Pokemon")


logger = logging.getLogger(__name__)

db = SQLAlchemy()


class Trainer(db.Model):
    __tablename__ = "trainer"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(128), index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey("pokemon.id"))

    def generate_token(self, expires_in: int = 3600) -> str:
        obj = {"id": self.id, "exp": time.time() + expires_in}
        return jwt.encode(obj, SECRET_KEY, algorithm="HS256")

    @classmethod
    def verify_token(token: str) -> Optional[Trainer]:
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.DecodeError as e:
            logger.error(e)
        else:
            return Trainer.query.get(data["id"])


class Pokemon(db.Model):
    __tablename__ = "pokemon"

    id = db.Column(db.Integer, primary_key=True)
    species_id = db.Column(db.String(64), index=True, nullable=False)
    name = db.Column(db.String(64), index=True, nullable=False)
    trainer = db.relationship("Trainer", backref="pokemon", lazy=True)

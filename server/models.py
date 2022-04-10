from __future__ import annotations
from typing import Optional
import logging
import time

from flask_sqlalchemy import SQLAlchemy

from .config import SECRET_KEY


__all__ = ("Trainer", "Pokemon")


logger = logging.getLogger(__name__)

db = SQLAlchemy()


class Trainer(db.Model):
    __tablename__ = "trainers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    password = db.Column(db.String(128))
    birthday = db.Column(db.Date())


class Pokemon(db.Model):
    __tablename__ = "pokemons"

    id = db.Column(db.Integer, primary_key=True)
    species_id = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    trainer = db.Column(db.String(64), db.ForeignKey("trainer.id"))

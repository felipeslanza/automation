from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from . import config
from .models import db


api = Flask(__name__)
api.config.from_object(config)
db.init_app(api)


@api.before_first_request
def initialize_database():
    db.create_all()


@api.route("/api", methods=["GET"])
def home():
    return "Welcome to PokeCode API!"


@api.route("/api/trainers", methods=["GET", "POST"])
def create_trainer():
    pass


@api.route("/api/trainers/<int:trainer_id>", methods=["GET", "PUT", "DELETE"])
def handle_trainer(trainer_id):
    if request.method == "GET":
        pass
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass

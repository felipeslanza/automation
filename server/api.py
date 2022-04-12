import logging

from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from . import config
from .models import db, Trainer, Pokemon


api = Flask(__name__)
api.config.from_object(config)
db.init_app(api)


# ++++++++++++++++++++
# Hooks
# ++++++++++++++++++++
@api.before_first_request
def initialize_database():
    db.create_all()


@api.before_request
def force_json_payload():
    if request.method in ("POST", "PUT") and not request.is_json:
        abort(
            400,
            description="Requests with payload require 'Content-Type: application/json'",
        )


# ++++++++++++++++++++
# Routes
# ++++++++++++++++++++
@api.route("/", methods=["GET"])
def home():
    return "Welcome to Pokemon API"


@api.route("/trainer", methods=["POST"])
def create_trainer():
    if request.method != "POST":
        err_msg = f"Invalid HTTP method {request.method})"
        api.logger.error(err_msg)
        abort(405, description=err_msg)

    try:
        email = request.json["email"]
        if Trainer.query.filter_by(email=email).first() is not None:
            err_msg = "Existing trainer"
            api.logger.error(err_msg)
            abort(400, description=err_msg)
        password = request.json["password"]
        name = request.json["name"]
        birthday = request.json["birthday"]
    except KeyError:
        err_msg = "Invalid or incomplete payload"
        api.logger.error(err_msg)
        abort(400, description=err_msg)
    else:
        trainer = Trainer(name=name, email=email, password=password, birthday=birthday)
        db.session.add(trainer)
        db.session.commit()
        return jsonify({"token": trainer.generate_token()}), 201


@api.route("/trainer/<int:trainer_id>", methods=["GET", "PUT", "DELETE"])
def handle_trainer(trainer_id):
    if request.method == "GET":
        trainer = Trainer.query.filter_by(id=str(trainer_id)).first()
        if trainer is None:
            abort(400, description=f"Trainer with id {trainer_id} not found")
        else:
            return jsonify(trainer.as_dict()), 200
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass

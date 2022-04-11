from dateutil import parser
import logging

from flask import Flask, abort, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

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
    # db.drop_all()
    db.create_all()


@api.before_request
def restrict_json_payload():
    if not request.is_json:
        abort(400)


# ++++++++++++++++++++
# Routes
# ++++++++++++++++++++
@api.route("/", methods=["GET"])
def home():
    return "Welcome to Pokemon API"


@api.route("/trainer", methods=["POST"])
def create_trainer():
    if request.method != "POST":
        api.logger.error(f"Invalid HTTP method {request.method}")
        abort(405)

    try:
        email = request.json["email"]
        if Trainer.query.filter_by(email=email).first() is not None:
            api.logger.error("Existing trainer")
            abort(400)

        name = request.json["name"]
        password = generate_password_hash(request.json["password"])
        birthday = parser.parse(request.json["birthday"]).date()
    except KeyError:
        api.logger.error("Invalid or incomplete payload")
        abort(400)
    except Exception as e:
        api.logger.error(e)
        abort(400)
    else:
        trainer = Trainer(name=name, email=email, password=password, birthday=birthday)
        db.session.add(trainer)
        db.session.commit()
        return jsonify({"token": trainer.generate_token()}), 201


@api.route("/trainer/<int:trainer_id>", methods=["GET", "PUT", "DELETE"])
def handle_trainer(trainer_id):
    if request.method == "GET":
        pass
    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass

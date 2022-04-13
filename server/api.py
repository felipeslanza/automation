from flask import Flask, abort, jsonify, request

from . import config
from .auth import auth
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
@api.route("/api", methods=["GET"])
def home():
    return "Welcome to Pokemon API"


@api.route("/api/login", methods=["POST"])
def get_token():
    try:
        email = request.json["email"]
        password = request.json["password"]
    except KeyError:
        abort(400, description="Invalid format")

    trainer = Trainer.query.filter_by(email=email).first()
    if trainer is None:
        abort(400, description="Trainer not found")

    if trainer.verify_password(str(password)):
        return jsonify({"token": trainer.generate_token()}), 200
    abort(401, description="Invalid credentials")


@api.route("/api/trainer", methods=["POST"])
def create_trainer():
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
        try:
            trainer = Trainer(
                name=name,
                email=email,
                password=password,
                birthday=birthday,
            )
        except Exception as e:
            api.logger.error(e)
        else:
            db.session.add(trainer)
            db.session.commit()
            return jsonify({"token": trainer.generate_token()}), 201


@api.route("/api/trainer/<int:trainer_id>", methods=["GET", "PUT", "DELETE"])
@auth.login_required
def handle_trainer(trainer_id: int):
    trainer = Trainer.query.get(trainer_id)
    if trainer is None:
        abort(400, description=f"Trainer with id {trainer_id} not found")

    if request.method == "GET":
        return jsonify(trainer.as_dict()), 200
    elif request.method == "PUT":
        for k, v in request.json.items():
            if k not in ("id", "password"):
                setattr(trainer, k, v)
        db.session.commit()
        return jsonify(success=True), 200
    elif request.method == "DELETE":
        db.session.delete(trainer)
        db.session.commit()
        return jsonify(success=True), 200


@api.route("/api/initials-pokemon", methods=["GET"])
def pokemon_rotation():
    pass


@api.route("/api/initials-pokemon/choose", methods=["POST"])
@auth.login_required
def pokemon_selection():
    pass

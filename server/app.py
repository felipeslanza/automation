import json

from flask import abort, jsonify, request, send_from_directory

from . import app, config
from .auth import auth
from .models import db, Trainer, Pokemon
from .rotation import get_random_rotation, pre_build_cache
from .utils import is_trainer_age_valid


# ++++++++++++++++++++
# Setup & Hooks
# ++++++++++++++++++++
db.init_app(app)


@app.before_first_request
def pre_start_hooks():
    pre_build_cache()
    db.create_all()


@app.before_request
def force_json_payload():
    if request.method in ("POST", "PUT") and not request.is_json:
        abort(
            400,
            description="Requests with payload require 'Content-Type: application/json'",
        )


# ++++++++++++++++++++
# Routes
# ++++++++++++++++++++
@app.route("/", methods=["GET"])
def serve():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/login", methods=["POST"])
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


@app.route("/api/trainer", methods=["POST"])
def create_trainer():
    try:
        email = request.json["email"]
        if Trainer.query.filter_by(email=email).first() is not None:
            err_msg = "Existing trainer"
            app.logger.error(err_msg)
            abort(400, description=err_msg)
        password = request.json["password"]
        name = request.json["name"]
        birthday = request.json["birthday"]
    except KeyError:
        abort(400, description="Invalid or incomplete payload")
    else:
        try:
            trainer = Trainer(
                name=name,
                email=email,
                password=password,
                birthday=birthday,
            )
        except Exception as e:
            app.logger.error(e)
            abort(400, description="Failed to create trainer")
        else:
            db.session.add(trainer)
            db.session.commit()
            return jsonify({"success": True, "token": trainer.generate_token()}), 201


@app.route("/api/trainer", methods=["GET", "PUT", "DELETE"])
@auth.login_required
def handle_trainer():
    trainer = auth.current_user()
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


@app.route("/api/initials-pokemon", methods=["GET"])
@auth.login_required
def pokemon_rotation():
    trainer = auth.current_user()
    try:
        pokemons = get_random_rotation(config.POKEMON_ALLOWED_STARTING_TYPES)
    except Exception as e:
        app.logger.error(e)
        abort(400, description="Service unavailable")
    else:
        trainer.last_rotation = json.dumps(pokemons, sort_keys=False)
        pokemons_arr = [(k, v) for k, v in pokemons.items()]
        # Must return an array to preserver sorting order
        return jsonify(pokemons_arr), 200


@app.route("/api/initials-pokemon/choose", methods=["POST"])
@auth.login_required
def pokemon_selection():
    trainer = auth.current_user()
    if trainer.pokemon_id:
        abort(400, description="You can only select a pokemon once!")

    if not is_trainer_age_valid(trainer.birthday):
        abort(400, description="Trainer's age must be above 14-years-old to proceed")

    if not trainer.last_rotation:
        abort(400, description="Must go through a rotation first!")

    rotation_obj = json.loads(trainer.last_rotation)
    species_id = request.json.get("selected_species_id")
    if species_id is None:
        abort(400, description="Payload missing selected pokemon")

    try:
        pokemon = Pokemon(species_id=int(species_id), name=rotation_obj[str(species_id)])
    except KeyError:
        abort(400, description="Must select a pokemon from the last rotation!")
    trainer.pokemon = pokemon
    db.session.add(pokemon)
    db.session.commit()

    return jsonify(success=True), 200

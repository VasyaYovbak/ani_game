from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import Session

from character_view.models import Anime
from connection import engine

anime_blueprint = Blueprint("anime", __name__)


def get_data_from(obj):
    data = {**obj.__dict__}
    del data['_sa_instance_state']
    return data


@anime_blueprint.route("/anime", methods=['GET'])
@jwt_required()
def get_anime_list():
    session = Session(bind=engine)
    anime_list = session.query(Anime).all()
    res = []

    for anime in anime_list:
        res.append(get_data_from(anime))

    return jsonify(res), 200


@anime_blueprint.route("/anime/<int:anime_id>", methods=['GET'])
@jwt_required()
def get_anime(anime_id):
    session = Session(bind=engine)
    anime = session.query(Anime).filter(Anime.anime_id == anime_id).first()

    return jsonify(get_anime_list(anime))

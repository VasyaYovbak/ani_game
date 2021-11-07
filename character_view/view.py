from marshmallow import ValidationError

from character_view.models import Character
from flask_restful import Resource
from flask import Blueprint, request, Response, redirect
from character_view.schema import character_schema
from connection import session
from game_view.models import Card

character_blueprint = Blueprint("character", __name__)


class CharacterBase(Resource):

    def get(self):
        characters = []
        for character in session.query(Character).all():
            character = character.__dict__
            del character['_sa_instance_state']
            characters.append(character)
        return str(characters), 200

    def post(self):
        try:
            for character in request.json:
                table_character = Character(**character_schema.load(character))
                if not session.query(Character).filter(Character.name == table_character.name).all():
                    session.add(table_character)
                else:
                    raise ValidationError(f'{table_character.name} already exists')
            session.commit()
            return "All Character successfully added", 200
        except ValidationError as e:
            return str(e.__dict__.get("messages")), 400


class CharacterCRUD(Resource):
    def get(self, character_id):
        character = session.query(Character).get(character_id).__dict__
        del character['_sa_instance_state']
        return str(character), 200

    def put(self, character_id):
        character = session.query(Character).get(character_id)
        if not character:
            return "Wrong Character id", 400

        new_character = Character(**character_schema.load(request.json))

        character.name = new_character.name
        character.image = new_character.image
        character.is_good = new_character.is_good
        character.is_alive = new_character.is_alive

        session.commit()

        return "Character info successfully changed ", 200

    def delete(self, character_id):
        character = session.query(Character).get(character_id)
        if not character:
            return "Wrong Achievement id", 400
        cards_with_character = session.query(Card).filter(Card.character_id == character_id).all()
        for card in cards_with_character:
            session.delete(card)
        session.commit()
        session.query(Character).filter(Character.character_id == character_id).delete()
        session.commit()
        return "Achievement successfully deleted", 200


character_blueprint.add_url_rule('/characters', view_func=CharacterBase.as_view("characterBase"))
character_blueprint.add_url_rule('/character/<int:character_id>', view_func=CharacterCRUD.as_view("characterCRUD"))

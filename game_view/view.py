import random
from time import sleep

import flask
import sqlalchemy
from flask import Blueprint, request, redirect
from flask_restful import Resource
from sqlalchemy.orm import Session

from character_view.models import Character
from connection import session, engine
from game_view.models import Game, UserQueue, Card
from flask_jwt_extended import jwt_required, get_jwt_identity

from user_view.models import User

game_blueprint = Blueprint("game", __name__)


@game_blueprint.route("/game/start", methods=['POST'])
@jwt_required()
def gameSearch():
    user_id = get_jwt_identity()

    user = session.query(User).get(user_id)

    available_user = session.query(UserQueue).filter(
        (user.rating + 300 >= UserQueue.rating) & (UserQueue.rating >= user.rating - 300)).first()

    if not available_user:
        waiting_user = UserQueue(user_id=user_id, rating=user.rating)
        session.add(waiting_user)
        session.commit()
        condition = True
        while condition:
            session.commit()
            available_user = session.query(UserQueue).filter(
                (user.rating + 300 >= UserQueue.rating) & (UserQueue.rating >= user.rating - 300)).first()
            if not available_user:
                condition = False
            sleep(1)
        game = session.query(Game).order_by(sqlalchemy.desc(Game.game_id)).first()
        session.close()
        return redirect(f"/game/{game.game_id}", code=307)
    else:
        session.query(UserQueue).filter(UserQueue.user_id == available_user.__dict__["user_id"]).delete()
        game = Game(loser_id=available_user.__dict__["user_id"], winner_id=user_id)
        session.add(game)
        session.commit()
        game = session.query(Game).order_by(sqlalchemy.desc(Game.game_id)).first()
        gameStart(game.game_id)
        return redirect(f"/game/{game.game_id}", code=307)


@game_blueprint.route("/game/<int:game_id>", methods=['POST'])
@jwt_required()
def getCards(game_id):
    user_id = get_jwt_identity()
    game = session.query(Game).get(game_id)
    players = [game.winner_id, game.loser_id]
    opponent = 0
    for player in players:
        if player != user_id:
            opponent = player
    result = []

    all_cards = session.query(Card).filter((Card.game_id == game_id) & (Card.user_id == user_id)).all()
    for card in all_cards:
        card = card.__dict__
        del card['_sa_instance_state'], card['is_selected_hero']
        result.append(card)

    selected_character = session.query(Card).filter(
        (Card.game_id == game_id) & (Card.user_id == opponent) & (Card.is_selected_hero == True)).first().__dict__
    del selected_character['_sa_instance_state']

    return str({"cards": result, "selected_character": selected_character})


def gameStart(game_id):
    COUNT_OF_CARDS = 3
    game = session.query(Game).get(game_id)
    character_list = session.query(Character).all()
    size = len(character_list)
    cards_id_1 = []
    cards_id_2 = []
    while len(cards_id_1) != COUNT_OF_CARDS:
        number = int(random.random() * size + 1)
        if number not in cards_id_1:
            cards_id_1.append(number)

    while len(cards_id_2) != COUNT_OF_CARDS:
        number = int(random.random() * size + 1)
        if number not in cards_id_2:
            cards_id_2.append(number)

    selected_hero_1 = random.choice(cards_id_1)
    selected_hero_2 = random.choice(cards_id_2)
    print(cards_id_1)
    print(selected_hero_1)
    print(cards_id_2)
    print(selected_hero_2)

    for i in range(COUNT_OF_CARDS):
        if cards_id_1[i] == selected_hero_1:
            card = Card(character_id=cards_id_1[i], is_active=True, user_id=game.winner_id, is_selected_hero=True,
                        game_id=game_id)
        else:
            card = Card(character_id=cards_id_1[i], is_active=True, user_id=game.winner_id, is_selected_hero=False,
                        game_id=game_id)
        session.add(card)

    for i in range(COUNT_OF_CARDS):
        if cards_id_2[i] == selected_hero_2:
            card = Card(character_id=cards_id_2[i], is_active=True, user_id=game.loser_id, is_selected_hero=True,
                        game_id=game_id)
        else:
            card = Card(character_id=cards_id_2[i], is_active=True, user_id=game.loser_id, is_selected_hero=False,
                        game_id=game_id)
        session.add(card)
    session.commit()

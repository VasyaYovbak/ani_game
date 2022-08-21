import json
import random
import datetime
from functools import wraps

import jwt
import flask
from flask_socketio import send, emit, join_room, leave_room
from config import Config
from connection import engine
from sqlalchemy.orm import Session

from game_view.models import Card, Game
from user_view.models import User

gamers = dict()
games = []


def login_required(f):
    @wraps(f)
    def decorated(message):
        try:
            data = jwt.decode(message['access_token'], Config.SECRET_KEY, algorithms=['HS256'])
        except Exception as e:
            print("error with jwt decode")
            return "Error(("
        return f(message, data['sub'])

    return decorated


def create_game(data):
    game = {
        "id": str(data['id']),
        "users": data['users'],
        "current_step": data['users'][random.randint(0, 1)]
    }
    games.append(game)


def get_current_game(game_id):
    session = Session(bind=engine)
    for game in games:
        if game['id'] == game_id:
            session.close()
            return game
    game = session.query(Game).filter(Game.game_id == game_id).first()
    session.close()
    if game is None:
        return "smf went wrong!!! this game hasn't started yet"
    if game.date:
        return "sorry, this game is over"
    create_game({
        "id": str(game_id),
        "users": [game.loser_id, game.winner_id],
    })
    for game in games:
        if game['id'] == game_id:
            return game


def get_opponent(game_id, user_id):
    game = get_current_game(game_id)
    for user in game['users']:
        if user != user_id:
            return user


def get_active_cards(cards):
    active = []
    for card in cards:
        if card['is_active']:
            active.append(card)
    return active


def setup_socket_game_logic(sio):
    @sio.on('connect')
    def handle_connect(massage):
        print(flask.request.sid)
        print('Client connected')

    @sio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @sio.on('connect-to-game')
    @login_required
    def connect(massage, user_id):
        data = massage['data']
        room_id = data['game_id']
        game = get_current_game(room_id)
        join_room(room_id)
        if type(game) == str:
            if game == "sorry, this game is over":
                session = Session(bind=engine)
                db_game = session.query(Game).filter(Game.game_id == room_id).first()
                winner = session.query(User).filter(User.id == db_game.winner_id).first()
                loser = session.query(User).filter(User.id == db_game.loser_id).first()
                emit('game_end', {"winner": winner.username, "loser": loser.username}, sid=flask.request.sid)
            emit("step_info", game, sid=flask.request.sid)
            return
        print(str(user_id) + ' has enter')
        if game['current_step'] != user_id:
            emit('change_turn', sid=flask.request.sid)

    @sio.on('step')
    @login_required
    def make_step(massage, user_id):
        game = get_current_game(massage['data']["game_id"])
        if type(game) == str:
            emit("step_info", game, sid=flask.request.sid)
            return
        if game["current_step"] != user_id:
            emit("step_info", "smf went wrong!!! It isn't your move", sid=flask.request.sid)
            return
        data = massage['data']
        cards = data['cards']
        active_cards = get_active_cards(cards)
        opponent_id = get_opponent(game["id"], user_id)
        session = Session(bind=engine)
        if len(active_cards) == 1:
            suggested_cart = session.query(Card).filter(
                (Card.game_id == game['id']) & (Card.user_id == user_id) & Card.is_selected_hero).first()
            if suggested_cart.card_id == active_cards[0]['card_id']:
                db_game = session.query(Game).filter(Game.game_id == game['id']).first()
                db_game.winner_id = user_id
                winner = session.query(User).filter(User.id == user_id).first()
                winner.rating += 25
                db_game.loser_id = opponent_id
                loser = session.query(User).filter(User.id == opponent_id).first()
                if loser.rating > 25:
                    loser.rating -= 25
                db_game.date = datetime.datetime.today()
                session.commit()
                winner = session.query(User).filter(User.id == db_game.winner_id).first()
                loser = session.query(User).filter(User.id == db_game.loser_id).first()
                emit('game_end', {"winner": winner.username, "loser": loser.username}, room=game['id'], broadcast=True)
                for this_game in games:
                    if this_game['id'] == game['id']:
                        games.remove(this_game)
                return
            else:
                emit("step_info", "Alas, this is not a selected character", sid=flask.request.sid)
                emit("change_turn", opponent_id, room=game["id"], broadcast=True)
        else:
            for new_card in cards:
                card = session.query(Card).filter(Card.card_id == new_card['card_id']).first()
                card.is_active = new_card['is_active']
                session.commit()
            emit("change_turn", opponent_id, room=game['id'], broadcast=True)
        session.close()
        game["current_step"] = opponent_id

    @sio.on("chat")
    @login_required
    def chat(message, user_id):
        session = Session(bind=engine)
        data = message['data']
        text = data['text']
        game_id = data['game_id']
        user = session.query(User).filter(User.id == user_id).first()
        game = session.query(Game).filter(Game.game_id == game_id).first()
        chat = json.loads(game.chat)
        chat.append({
            "text": text,
            "username": user.username
        })
        game.chat = json.dumps(chat)
        session.commit()
        emit("chat", {
            "text": text,
            "username": user.username
        }, room=game_id)
        session.close()

    @sio.on("connectToChat")
    @login_required
    def chat(message, user_id):
        session = Session(bind=engine)
        data = message['data']
        game_id = data['game_id']
        game = session.query(Game).filter(Game.game_id == game_id).first()
        chat = json.loads(game.chat)
        for massage in chat:
            print({
                "text": massage['text'],
                "username": massage['username']
            })
            emit("chat", {
                "text": massage['text'],
                "username": massage['username']
            }, sid=flask.request.sid)
        session.close()

from functools import wraps

import flask
import sqlalchemy
from flask import request, Blueprint, jsonify
from flask_socketio import join_room, emit, leave_room

import jwt
from config import Config
from connection import engine
from sqlalchemy.orm import Session
from game_view.models import GameRoom, Game, RoomsAnimeList
from flask_jwt_extended import jwt_required, get_jwt_identity

from game_view.schema import create_room_schema
from game_view.view import gameStart
from user_view.models import User

rooms_blueprint = Blueprint("room", __name__, url_prefix='/room')


# def get_data_from(obj):
#     data = {**obj.__dict__}
#     del data['_sa_instance_state']
#     return data

def get_clear_object_from_db(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d


# def get_room_with_users_info(room):
#     session = Session(bind=engine)
#     if room['creator_user_id'] != "None":
#         print(room['creator_user_id'])
#         user = session.query(User).filter(User.id == room['creator_user_id']).first()
#         room['creator_image'] = user.image
#         room['creator_nickname'] = user.username
#         del room['creator_user_id']
#     if room['second_user_id'] != "None":
#         user = session.query(User).filter(User.id == room['second_user_id']).first()
#         room['second_user_image'] = user.image
#         room['second_user_nickname'] = user.username
#         del room['second_user_id']
#
#     return room


def get_rooms_info(rooms):
    session = Session(bind=engine)
    user_ids = set()
    for room in rooms:
        user_ids.add(room['creator_user_id'])
        if room['second_user_id'] != "None":
            user_ids.add(room['second_user_id'])
    users = session.query(User).filter(User.id.in_(user_ids)).all()
    users_dict = dict()
    for user in users:
        users_dict[str(user.id)] = user.username

    for room in rooms:
        anime_list_db = session.query(RoomsAnimeList).filter(RoomsAnimeList.room_id == room['room_id']).all()
        anime_list = []
        for anime in anime_list_db:
            anime_list.append(anime.anime_id)
        room['anime_list'] = anime_list

        room['creator_user'] = users_dict[room['creator_user_id']]
        if room['second_user_id'] != "None":
            room['second_user'] = users_dict[room['second_user_id']]
        del room['creator_user_id'], room['second_user_id']

    session.close()
    return rooms


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


def setup_rooms_logic(sio):
    @sio.on('room-connect')
    def connect(message):
        room_id = message['data']
        room_id = f'room{room_id}'
        join_room(room_id)

    @sio.on('room-create.py')
    @login_required
    def createRoom(message, user_id):
        data = message['data']

        session = Session(bind=engine)
        new_game_room = GameRoom(**create_room_schema.load({'name': data['name']}))
        new_game_room.creator_user_id = user_id
        new_game_room.is_game_started = False
        session.add(new_game_room)
        session.commit()

        for anime_id in data['animeList']:
            room_anime = RoomsAnimeList(room_id=new_game_room.room_id, anime_id=int(anime_id))
            session.add(room_anime)

        session.commit()

        emit('room-info',
             {'event': 'create.py', 'data': {'room': get_rooms_info([get_clear_object_from_db(new_game_room)])[0]}})
        sio.emit('rooms',
                 {'add': get_rooms_info([get_clear_object_from_db(new_game_room)]), 'remove': [], 'update': []})
        session.close()


    @sio.on('room-update')
    @login_required
    def update(message, user_id):
        data = message['data']
        session = Session(bind=engine)
        room = session.query(GameRoom).filter(GameRoom.room_id == data['room_id']).first()
        if data['animeList']:
            session.query(RoomsAnimeList).filter(RoomsAnimeList.room_id == room.room_id).delete()
            session.commit()

            for anime_id in data['animeList']:
                room_anime = RoomsAnimeList(room_id=room.room_id, anime_id=int(anime_id))
                session.add(room_anime)
            session.commit()

        if data['name']:
            room.name = data['name']
            session.commit()

        emit('room-info',
             {'event': 'update', 'data': {'room': get_rooms_info([get_clear_object_from_db(room)])[0]}})
        sio.emit('rooms', {'add': [], 'remove': [], 'update': get_rooms_info([get_clear_object_from_db(room)])}, )
        session.close()

    @sio.on('room-join')
    @login_required
    def join(message, user_id):
        data = message['data']
        session = Session(bind=engine)
        room = session.query(GameRoom).filter(GameRoom.room_id == data['room_id']).first()
        if room.creator_user_id == user_id or room.second_user_id == user_id:
            emit('room-info', {'event': 'join', 'data': {'room': get_rooms_info([get_clear_object_from_db(room)])[0]}})
            return

        if room.second_user_id:
            emit('room-info', {'event': 'error', 'message': "Sorry this room already full"}, sid=flask.request.sid)
            return

        room.second_user_id = user_id
        session.commit()

        game = Game(loser_id=room.second_user_id, winner_id=room.creator_user_id, chat='[]')
        session.add(game)
        session.commit()
        game = session.query(Game).order_by(sqlalchemy.desc(Game.game_id)).first()

        anime_list_db = session.query(RoomsAnimeList).filter(RoomsAnimeList.room_id == data['room_id']).all()
        anime_ids = []
        for anime in anime_list_db:
            anime_ids.append(anime.anime_id)

        gameStart(game.game_id, anime_ids)

        room.is_game_started = True
        sio.emit('rooms', {'add': [], 'remove': [get_clear_object_from_db(room)], 'update': []}, )
        session.query(RoomsAnimeList).filter(RoomsAnimeList.room_id == data['room_id']).delete()
        session.delete(room)
        session.commit()
        emit('room-info', {'event': 'gameStart', 'data': {'game_id': game.game_id}}, room=f'room{data["room_id"]}')

        # emit('room-info', {'event': 'join', 'data': {'room': get_rooms_info([get_clear_object_from_db(room)])[0]}},
        #      room=f'room{data["room_id"]}')
        # sio.emit('rooms', {'add': [], 'remove': [], 'update': get_rooms_info([get_clear_object_from_db(room)])}, )
        # join_room(f'room{data["room_id"]}')
        session.close()

    @sio.on('room-leave')
    @login_required
    def leave(message, user_id):
        data = message['data']
        session = Session(bind=engine)
        room = session.query(GameRoom).filter(GameRoom.room_id == data['room_id']).first()

        if room.creator_user_id != user_id and room.second_user_id != user_id:
            emit('room-info', {'event': 'error', 'message': "You can't leave before you join it"})
            return

        if room.second_user_id == user_id:
            sio.emit('rooms', {'add': [], 'remove': [], 'update': get_rooms_info([get_clear_object_from_db(room)])}, )
            room.second_user_id = None

        if room.creator_user_id == user_id:
            if room.second_user_id:
                room.creator_user_id = room.second_user_id
                sio.emit('rooms',
                         {'add': [], 'remove': [], 'update': get_rooms_info([get_clear_object_from_db(room)])}, )
            else:
                room.creator_user_id = None
                sio.emit('rooms', {'add': [], 'remove': [get_clear_object_from_db(room)], 'update': []}, )
                session.delete(room)

        session.commit()

        emit('room-info', {'event': 'leave', 'data': {'room': get_rooms_info([get_clear_object_from_db(room)])[0]}},
             room=f'room{data["room_id"]}')
        leave_room(f'room{data["room_id"]}')
        session.close()

    @sio.on('room-start')
    @login_required
    def startRoom(message, user_id):
        data = message['data']

        session = Session(bind=engine)
        room = session.query(GameRoom).filter(GameRoom.room_id == data['room_id']).first()

        if room.creator_user_id != user_id:
            emit('room-info', {'event': 'error', 'message': "Sorry you can't start this game (you are not creator)"})
            return

        game = Game(loser_id=room.second_user_id, winner_id=room.creator_user_id, chat='[]')
        session.add(game)
        session.commit()
        game = session.query(Game).order_by(sqlalchemy.desc(Game.game_id)).first()

        anime_list_db = session.query(RoomsAnimeList).filter(RoomsAnimeList.room_id == data['room_id']).all()
        anime_ids = []
        for anime in anime_list_db:
            anime_ids.append(anime.anime_id)

        gameStart(game.game_id, anime_ids)

        room.is_game_started = True
        sio.emit('rooms', {'add': [], 'remove': [get_clear_object_from_db(room)], 'update': []}, )
        session.delete(room)
        session.commit()
        emit('room-info', {'event': 'gameStart', 'data': {'game_id': game.game_id}}, room=f'room{data["room_id"]}')
        session.close()

    @sio.on('rooms-get')
    @login_required
    def getRooms(message, user_id):
        session = Session(bind=engine)
        rooms = session.query(GameRoom).filter(GameRoom.is_game_started == False).all()

        res = []
        for room in rooms:
            res.append(get_clear_object_from_db(room))

        emit('rooms', {'add': get_rooms_info(res), 'remove': [], 'update': []})
        session.close()

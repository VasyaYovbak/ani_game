from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_socketio import SocketIO, emit, send

from connection import session
from flask_jwt_extended import JWTManager
from config import Config
from game_view.game_logic import setup_socket_game_logic
from game_view.rooms_logic import rooms_blueprint, setup_rooms_logic
from user_view.models import TokenBlocklist

app = Flask(__name__)
CORS(app, resources='*')
sio = SocketIO(app, logger=True, cors_allowed_origins='*', async_mode="threading")

api = Api(app)

jwt = JWTManager(app)

setup_socket_game_logic(sio)
setup_rooms_logic(sio)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    session.commit()
    token = session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


app.config.from_object(Config)

from user_view.view import user_info

from character_view.view import character_blueprint
from game_view.view import game_blueprint
from game_view.anime import anime_blueprint

# from database_test import database_test, session
# app.register_blueprint(database_test)


app.register_blueprint(user_info)
app.register_blueprint(character_blueprint)
app.register_blueprint(game_blueprint)
app.register_blueprint(rooms_blueprint)
app.register_blueprint(anime_blueprint)

if __name__ == '__main__':
    sio.run(app, debug=True, port=2012)

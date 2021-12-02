from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from hello_student import HelloWorld
from flask_jwt_extended import JWTManager
from config import Config
from user_view.models import TokenBlocklist
from flask_socketio import SocketIO, send, emit, join_room

app = Flask(__name__)
CORS(app, resources='*')
api = Api(app)
socketio = SocketIO(app)

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    session.commit()
    token = session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


app.config.from_object(Config)

api.add_resource(HelloWorld, '/api/v1/hello-world-<int:variant>')


@socketio.on('join__room')
def join__room(data, *args):  # game id
    join_room(data['room'])


@socketio.on('question')
def send_question(data, *args):
    room = data['room']
    emit("my response", data, to=room, broadcast=False)


from user_view.view import user_info
from database_test import database_test, session
from character_view.view import character_blueprint
from game_view.view import game_blueprint

app.register_blueprint(database_test)
app.register_blueprint(user_info)
app.register_blueprint(character_blueprint)
app.register_blueprint(game_blueprint)

if __name__ == '__main__':
    socketio.run(app, debug=True, log_output=True)

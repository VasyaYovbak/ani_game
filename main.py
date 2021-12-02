from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from connection import session
from hello_student import HelloWorld
from flask_jwt_extended import JWTManager
from config import Config
from user_view.models import TokenBlocklist

app = Flask(__name__)
CORS(app, resources='*')
api = Api(app)

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    session.commit()
    token = session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


app.config.from_object(Config)

api.add_resource(HelloWorld, '/api/v1/hello-world-<int:variant>')

from user_view.view import user_info

from character_view.view import character_blueprint
from game_view.view import game_blueprint

# from database_test import database_test, session
# app.register_blueprint(database_test)

app.register_blueprint(user_info)
app.register_blueprint(character_blueprint)
app.register_blueprint(game_blueprint)

if __name__ == '__main__':
    app.run(debug=True, port=2012)

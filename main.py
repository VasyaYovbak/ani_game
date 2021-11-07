from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from hello_student import HelloWorld
from flask_jwt_extended import JWTManager
from config import Config

app = Flask(__name__)
CORS(app, resources='*')
api = Api(app)
jwt = JWTManager(app)
app.config.from_object(Config)


api.add_resource(HelloWorld, '/api/v1/hello-world-<int:variant>')

from user_view.view import user_info
from database_test import database_test
from character_view.view import character_blueprint

app.register_blueprint(database_test)
app.register_blueprint(user_info)
app.register_blueprint(character_blueprint)


if __name__ == '__main__':
    app.run(debug=True, port=2012)

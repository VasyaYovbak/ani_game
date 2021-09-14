from flask import Flask
from flask_restful import Resource, Api

from hello_student import HelloWorld


app = Flask(__name__)
api = Api(app)

api.add_resource(HelloWorld, '/api/v1/hello-world-<int:variant>')

if __name__ == '__main__':
    app.run(debug=True)

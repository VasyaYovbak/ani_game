from models import ResponseModel, Client
import logging
from jsonschema import validate
from connection import session
from user_view.models import TokenBlocklist, User
logger = logging.getLogger("test_user")


def is_refresh_revoked(jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_type = jwt_payload["type"]
    expired = jwt_payload["exp"]

    if token_type != "refresh":
        raise Exception("Invalid token type, this method needs refresh token")

    if expired == 0:
        raise Exception("Token already expired, enter valid one")

    token = session.query(TokenBlocklist.id).filter_by(jti=jti).first()

    if isinstance(token, str):
        raise Exception("Refresh token is invalid")

    if token == 0:
        raise Exception("Refresh token is invalid")

    return True


def is_user_added_to_db(body: dict):

    email = body['email']
    user = session.query(User).filter(User.email == email).first()

    if user is None:
        return False

    return True


class Register:

    def __init__(self):
        self.client = Client()

    def register_user(self, body: dict, schema: dict):
        response = self.client.custom_request("POST", 'http://127.0.0.1:5000/registration', json=body)
        validate(instance=response.json(), schema=schema)
        logger.info("response.text")
        return ResponseModel(status_code=response.status_code, response=response.json())


class Login:

    def __init__(self):
        self.client = Client()

    def login_user(self, body: dict, schema: dict):
        response = self.client.custom_request("POST", 'http://127.0.0.1:5000/login', json=body)
        validate(instance=response.json(), schema=schema)
        logger.info("response.text")
        return ResponseModel(status_code=response.status_code, response=response.json())


class Logout:

    def __init__(self):
        self.client = Client()

    def logout_user(self, body: dict, schema: dict, access_token: str):
        response = self.client.custom_request("POST", 'http://127.0.0.1:5000/logout', headers={"Authorization": "Bearer " + access_token}, json=body)
        validate(instance=response.json(), schema=schema)
        logger.info("response.text")
        return ResponseModel(status_code=response.status_code, response=response.json())


class RefreshToken:

    def __init__(self):
        self.client = Client()

    def refresh_token(self, body=dict, schema=dict):
        response = self.client.custom_request("POST", 'http://127.0.0.1:5000/refresh_tokens', json=body)
        validate(instance=response.json(), schema=schema)
        logger.info("response.text")
        return ResponseModel(status_code=response.status_code, response=response.json())


class SendEmailConfirmation:

    def __init__(self):
        self.client = Client()

    def send_email_confirmation(self, body=dict, schema=dict):
        response = self.client.custom_request("POST", 'http://127.0.0.1:5000/verify_email', json=body)
        validate(instance=response.json(), schema=schema)
        logger.info("response.text")
        return ResponseModel(status_code=response.status_code, response=response.json())


class ConfirmEmail:

    def __init__(self):
        self.client = Client()

    def confirm_email(self, schema=dict, url=str):
        response = self.client.custom_request("GET", url=url)
        validate(instance=response.json(), schema=schema)
        logger.info("response.text")
        return ResponseModel(status_code=response.status_code, response=response.json())


class SendEmailReset:

    def __init__(self):
        self.client = Client()

    def send_email_reset(self, body=dict, schema=dict):
        response = self.client.custom_request("POST", 'http://127.0.0.1:5000/send_reset_list', json=body)
        validate(instance=response.json(), schema=schema)
        logger.info("response.text")
        return ResponseModel(status_code=response.status_code, response=response.json())


class ResetPassword:

    def __init__(self):
        self.client = Client()

    def reset_password(self, body=dict, schema=dict, url=str):
        response = self.client.custom_request("POST", url=url, json=body)
        validate(instance=response.json(), schema=schema)
        logger.info("response.text")
        return ResponseModel(status_code=response.status_code, response=response.json())
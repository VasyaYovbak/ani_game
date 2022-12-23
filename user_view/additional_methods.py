from sendgrid import sendgrid
from config import SendGridApi_key
from datetime import datetime, timezone
from connection import session
from user_view.models import TokenBlocklist, User
from marshmallow import ValidationError
from user_view.redis_connection import r
from flask import url_for
from sendgrid.helpers.mail import Mail
from redis.commands.json.path import Path


def send_email(message):
    try:
        sg = sendgrid.SendGridAPIClient(SendGridApi_key.API_KEY)
        response = sg.send(message)
        code, body, headers = response.status_code, response.body, response.headers
        print(f"Response code: {code}")
        print(f"Response headers: {headers}")
        print(f"Response body: {body}")
    except:
        raise Exception("Email have not been sent")

    return response


def revoke_refresh_token(decoded_refresh):
    jti_refresh = decoded_refresh["jti"]
    refresh_token_type = decoded_refresh["type"]
    now = datetime.now(timezone.utc)

    session.add(TokenBlocklist(jti=jti_refresh, type=refresh_token_type, created_at=now))
    session.commit()


def revoke_access_token(jwt_payload: dict):

    jti_access = jwt_payload["jti"]
    token_type = jwt_payload["type"]
    expired = jwt_payload["exp"]

    token = {
        'jti': jti_access,
        'type': token_type,
        'expired': expired
    }

    r.json().set(jti_access, Path.root_path(), token)


# This method is responsible for checking if refresh token is revoked or not
def is_refresh_valid(jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_type = jwt_payload["type"]

    if token_type != "refresh":
        raise Exception("Invalid token type, this method needs refresh token")

    token = session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    if token is not None:
        raise Exception("Refresh token already revoked")

    return True


# This method is responsible for checking if access token is revoked or not
def is_access_valid(jwt_payload: dict):
    jti_access = jwt_payload["jti"]
    token_type = jwt_payload["type"]

    if token_type != "access":
        raise ValidationError("Invalid token type, this method needs access token")

    token = r.json().get(jti_access)

    if token is not None:
        raise Exception("Access token already revoked")

    return True


def send_registration_email(email, send_token):

    confirm_url = url_for('user_info.confirm_email', token=send_token, _external=True)

    template_id = "d-158e896d27074481a8916af25a935551"

    message = Mail(from_email="anigamegroup@gmail.com",
                   to_emails=email)
    message.dynamic_template_data = {
        'text': 'Verify your email!',
        'url': confirm_url,
    }
    message.template_id = template_id

    return send_email(message)




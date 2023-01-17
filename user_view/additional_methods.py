from sendgrid import sendgrid
from config import SendGridApi_key
from datetime import datetime, timezone, timedelta
from connection import session
from user_view.models import TokenBlocklist, User
from marshmallow import ValidationError
from user_view.redis_connection import r, r2
from flask import url_for
from sendgrid.helpers.mail import Mail
from redis.commands.json.path import Path
import random
import string
from faker import Faker


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

    r.setex(
        jti_access,
        timedelta(minutes=3),
        value=jti_access
    )


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

    token = r.get(jti_access)

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


def generate_random_password():
    letters = ''.join((random.choice(string.ascii_letters) for i in range(17)))
    digits = ''.join((random.choice(string.digits) for i in range(11)))

    sample_list = list(letters + digits)
    random.shuffle(sample_list)

    final_string = ''.join(sample_list)

    return final_string


def get_data_for_guest():

    number = [5, 6, 7, 8, 9, 10, 11, 12]
    get_random_number = random.choice(number)

    endings = ["com", "org", "net"]

    random_digits = ''.join((random.choice(string.digits) for i in range(16)))
    letters = ''.join((random.choice(string.ascii_letters) for i in range(get_random_number)))
    ending = random.choice(endings)

    username = f"GuestUsername{random_digits}"
    email = f"GuestEmailAddress@{letters}.{ending}"
    password = generate_random_password()

    return {"username": username, "email": email, "password": password}


from datetime import timedelta, datetime, timezone
import jwt as jwt1
from flask import Blueprint, request, jsonify, url_for
from app import app
from passlib.hash import argon2
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
import sendgrid
from sendgrid.helpers.mail import Mail
from connection import session
from user_view.models import User, TokenBlocklist
from user_view.validation import password_check, username_check, email_check
from marshmallow import ValidationError
from config import Config, SendGridApi_key
from user_view.redis_connection import jwt_redis_blacklist


ACCESS_EXPIRES = timedelta(minutes=3)


user_info = Blueprint('user_info', __name__)

mail = Mail(app)
STS = URLSafeTimedSerializer(Config.SECRET_KEY)


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


# This method is responsible for checking if refresh token is revoked or not
def is_refresh_valid(jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_type = jwt_payload["type"]
    expired = jwt_payload["exp"]

    if token_type != "refresh":
        raise Exception("Invalid token type, this method needs refresh token")

    if expired == 0:
        raise Exception("Token already expired, enter valid one")

    token = session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    if token is not None:
        raise Exception("Refresh token already revoked")

    return True


# This method is responsible for checking if access token is revoked or not
def is_access_valid(jwt_payload: dict):
    jti_access = jwt_payload["jti"]
    token_type = jwt_payload["type"]
    expired = jwt_payload["exp"]

    if token_type != "access":
        raise ValidationError("Invalid token type, this method needs access token")

    if expired == 0:
        raise Exception("Token already expired, enter valid one")

    token = jwt_redis_blacklist.get(name=jti_access)

    if token is not None:
        raise Exception("Access token already revoked")

    return True


# This method made for refreshing tokens
class TokenRefresh(Resource):

    def post(self):
        refresh_token = request.json.get("refresh_token")

        if len(refresh_token) == 0:
            raise Exception("This field cannot be empty, please enter valid refresh_token")

        decoded_refresh = jwt1.decode(refresh_token, Config.SECRET_KEY, algorithms=["HS256"])

        is_refresh_valid(decoded_refresh)
        user = session.query(User).filter(User.id == f'{decoded_refresh["sub"]}').first()

        tokens = user.get_tokens()

        now = datetime.now(timezone.utc)
        token_type = decoded_refresh['type']
        session.add(TokenBlocklist(jti=decoded_refresh['jti'], type=token_type, created_at=now))
        session.commit()

        return tokens


# This is registration method
class RegisterApi(Resource):

    def post(self):

        if "Authorization" in request.headers.keys():
            raise Exception("405:Sorry, you can't register now. Please first logout")

        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')

        username_check(username)
        email_check(email)
        password_check(password)

        user = User(username=username, email=email, password=password)

        if session.query(User).filter(User.email == f'{user.email}').count() or \
                session.query(User).filter(User.username == f'{user.username}').count():
            raise Exception("409:User with this email or username already registered")

        session.add(user)
        session.commit()

        tokens = user.get_tokens()
        user = user.__dict__
        del user['password'], user['_sa_instance_state'], user['permission']
        tokens['user'] = user

        return jsonify(tokens), 201


# This is login method
class LoginApi(Resource):

    def post(self):

        if "Authorization" in request.headers.keys():
            raise Exception("405:Sorry, you can't login now. Please first logout")

        email = request.json.get('email')
        password = request.json.get('password')
        username = request.json.get('username')

        login_data = User(username=username, email=email, password=password)

        user = session.query(User).filter(User.email == login_data.email).first()

        if not user:
            raise Exception('Wrong user email')
        if not argon2.verify(password, user.password):
            raise Exception('Wrong user password')

        tokens = user.get_tokens()
        user = user.__dict__
        del user['password'], user['_sa_instance_state'], user['permission']
        tokens['user'] = user
        return jsonify(tokens), 200


# This method is intended for user validation his email, it is generating special confirmation link and sending this link to you email with special template
class EmailVerification(Resource):

    def post(self):
        email = request.json.get("email")

        user = session.query(User).filter(User.email == email).first()
        if user == None:
            raise Exception("User with this email is not registered")

        token = user.get_verify_token()
        confirm_url = url_for('user_info.confirm_email', token=token, _external=True)

        template_id = "d-9b6742a4eab545d5819cf658be051f61"

        message = Mail(from_email="romaostrovskiy616@gmail.com",
                       to_emails=email)
        message.dynamic_template_data = {
            'text': 'Verify your email!',
            'url': confirm_url,
        }
        message.template_id = template_id

        return jsonify({"Message": str(send_email(message).status_code), "url": confirm_url}), 202


# This method cheking if you clicked on special link from method above, if yes then youre confirmed
@user_info.route('/confirm/<token>')
def confirm_email(token):

    decoded_verify = jwt1.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    user = session.query(User).filter(User.id == f'{decoded_verify["sub"]}').first()

    if user.confirmed:
        raise Exception('Account already confirmed. Please login.')

    is_refresh_valid(decoded_verify)

    now = datetime.now(timezone.utc)

    user.confirmed = True
    user.confirmed_on = now

    revoke_refresh_token(decoded_verify)

    session.add(user)
    session.commit()

    response = {'Message': 'You have confirmed your account. Thanks!'}
    return jsonify(response), 200


# This method responsible for sending password reset messages
class ResetPassword(Resource):

    def post(self):
        email = request.json.get("email")

        user = session.query(User).filter(User.email == email).first()
        if user == None:
            raise Exception("User with this email is not registered")

        token = user.get_reset_token()
        reset_url = url_for('user_info.reset_password', token=token, _external=True)

        template_id = "d-f6f22043bd8f4459b73beaee98e1b848"

        message = Mail(from_email="romaostrovskiy616@gmail.com",
                       to_emails=email)
        message.dynamic_template_data = {
            'text': "Reset password!",
            'url': reset_url,
            'url1': reset_url,
        }
        message.template_id = template_id

        return jsonify({"Message": str(send_email(message).status_code), "url": reset_url}), 202


# This Method responsible for reseting password
@user_info.route('/reset/<token>', methods=['POST'])
def reset_password(token):

    decoded_reset = jwt1.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
    user = session.query(User).filter(User.id == f'{decoded_reset["sub"]}').first()

    is_refresh_valid(decoded_reset)

    new_password = request.json["password"]
    password_check(new_password)

    session.query(User).filter(User.id == user.id).update(
        {"password": str(argon2.using(rounds=5).hash(new_password))})
    session.commit()

    revoke_refresh_token(decoded_reset)

    response = {"Message": "Password successfully changed"}
    return jsonify(response), 200


# This method responsible for logout
class Logout(Resource):

    @jwt_required()
    def post(self):

        refresh_token = request.json.get("refresh_token")
        if refresh_token == '':
            raise Exception("Refresh token is required")

        access_token = get_jwt()

        decoded_refresh = jwt1.decode(refresh_token, Config.SECRET_KEY, algorithms=["HS256"])

        is_refresh_valid(jwt_payload=decoded_refresh)
        is_access_valid(jwt_payload=access_token)

        jti_access = access_token["jti"]
        access_token_type = access_token["type"]

        revoke_refresh_token(decoded_refresh)

        jwt_redis_blacklist.set(name=jti_access, value=jti_access, ex=ACCESS_EXPIRES)
        jwt_redis_blacklist.close()

        return jsonify(
            msg=f"Refresh token and {access_token_type} token were successfully revoked, you are logged out!")


# class AchievementsBase(Resource):
#     def get(self):
#
#         result = []
#         achievements = session.query(Achievement).all()
#         if not achievements:
#             raise Exception(f'400:Got problem with taking Achievements (Achievement table is empty)')
#         for achievement in achievements:
#             achievement = achievement.__dict__
#             del achievement['_sa_instance_state']
#             result.append(achievement)
#         return jsonify(result), 200
#
#
#     @jwt_required()
#     def post(self):
#
#         permission = session.query(User.permission).filter(User.id == get_jwt_identity()).first()
#         if permission[0] != 'admin':
#             raise Exception("403:You dont have permissions to make this operation")
#         achievements = request.json
#         for achievement in achievements:
#             table_achievement = Achievement(**newAchievement.load(achievement))
#             if not session.query(Achievement).filter(Achievement.name == table_achievement.name).all():
#                 session.add(table_achievement)
#             else:
#                 raise Exception(f'409:{table_achievement.name} already exists')
#         session.commit()
#         return "All Achievement successfully added ", 200

#
# class AchievementCRUD(Resource):
#     def get(self, achievement_id):
#
#         achievement = session.query(Achievement).get(achievement_id)
#         if not achievement:
#             raise Exception("400:Sorry , this Achievement doesn't exists")
#         achievement = achievement.__dict__
#         del achievement['_sa_instance_state']
#         return jsonify(achievement), 200
#
#
#     @jwt_required()
#     def put(self, achievement_id):
#
#         permission = session.query(User.permission).filter(User.id == get_jwt_identity()).first()
#         if permission[0] != 'admin':
#             raise Exception("403:You dont have permissions to make this operation")
#         achievement = session.query(Achievement).get(achievement_id)
#         if not achievement:
#             raise Exception("404:Wrong Achievement id (Achievement doesn't exist)")
#         new_achievement = Achievement(**newAchievement.load(request.json))
#         achievement.name = new_achievement.name
#         achievement.description = new_achievement.description
#         achievement.experience = new_achievement.experience
#         session.commit()
#         return "Achievement successfully changed ", 200
#
#
#     @jwt_required()
#     def delete(self, achievement_id):
#
#         permission = session.query(User.permission).filter(User.id == get_jwt_identity()).first()
#         if permission[0] != 'admin':
#             raise Exception("403:You dont have permissions to make this operation")
#         achievement = session.query(Achievement).get(achievement_id)
#         if not achievement:
#             raise Exception("404:Wrong Achievement id (Achievement doesn't exist)")
#
#         user_achievements = session.query(UserAchievement).filter(
#             UserAchievement.achievement_id == achievement_id).all()
#         for user_achievement in user_achievements:
#             session.delete(user_achievement)
#         session.commit()
#
#         session.query(Achievement).filter(Achievement.id == achievement_id).delete()
#         session.commit()
#         return "Achievement successfully deleted", 200
#
#
@user_info.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    #last 5 games of current player and get data (opp and win or lose)
    user_info = session.query(User.email, User.username).filter(User.id == user_id).first()
    if not user_info:
        raise Exception("404:User doesn't exist")
    response = dict()

    response.setdefault('user_info', {"email": user_info[0],
                                      "username": user_info[1]})

    return jsonify(response), 200


# @user_info.route('/profile/change/password', methods=['PUT'])
# @jwt_required()
# def change_password():  # check old_password
#     user_id = get_jwt_identity()
#     old_password = session.query(User.password).filter(User.id == user_id)
#     info = request.json
#     if not bcrypt.verify(info['old_password'], old_password[0][0]):
#         return jsonify({"msg": "old_password is not correct"})
#     session.query(User).filter(User.id == user_id).update({"password": str(bcrypt.hash(info['new_password']))})
#     session.commit()
#     return jsonify({"msg": "Password successfully changed"}), 200
#
#
@user_info.route('/profile/change', methods=['PUT'])
@jwt_required()
def change():
    user_id = get_jwt_identity()
    for data in request.json:
        if data == "image":
            session.query(User).filter(User.id == user_id).update({"image": str(request.json["image"])})
        if data == "username":
            session.query(User).filter(User.id == user_id).update({"username": str(request.json["username"])})
    session.commit()
    return "All info changed successfully", 200


user_info.add_url_rule('/refresh_tokens', view_func=TokenRefresh.as_view("refresh_tokens"))
user_info.add_url_rule('/registration', view_func=RegisterApi.as_view("registration"))
user_info.add_url_rule('/login', view_func=LoginApi.as_view("login"))
user_info.add_url_rule('/logout', view_func=Logout.as_view("logout"))
user_info.add_url_rule('/verify_email', view_func=EmailVerification.as_view("verify_email"))
user_info.add_url_rule('/send_reset_list', view_func=ResetPassword.as_view("send_reset_list"))

# user_info.add_url_rule('/achievements', view_func=AchievementsBase.as_view("achievements_base"))
# user_info.add_url_rule('/achievement/<int:achievement_id>', view_func=AchievementCRUD.as_view("achievementCRUD"))

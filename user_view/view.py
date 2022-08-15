from datetime import timedelta, datetime, timezone
import jwt as jwt1
from flask import Blueprint, request, Response, redirect, jsonify

from flask_restful import Resource
from passlib.hash import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

from connection import session
from user_view.models import User,  TokenBlocklist
from user_view.schema import register_schema, login_schema
from marshmallow import ValidationError
from config import Config


JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=15)
EXPIRE = timedelta(days=1)

user_info = Blueprint('user_info', __name__)


def is_refresh_revoked(jwt_payload: dict):

    jti = jwt_payload["jti"]
    token_type = jwt_payload["type"]

    if token_type != "refresh":
        raise ValidationError("Invalid token type!!! Get the fuck out of here")

    token = session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    if token is not None:
        raise ValidationError("Token is invalid")


class TokenRefresh(Resource):


    def post(self):

        refresh_token = request.json.get("refresh_token")

        decoded_refresh = jwt1.decode(refresh_token, Config.SECRET_KEY, algorithms=["HS256"])

        is_refresh_revoked(decoded_refresh)
        user = session.query(User).filter(User.id == f'{decoded_refresh["sub"]}').first()

        tokens = user.get_tokens()

        now = datetime.now(timezone.utc)
        token_type = decoded_refresh['type']
        session.add(TokenBlocklist(jti=decoded_refresh['jti'], type=token_type, created_at=now))

        return tokens


class RegisterApi(Resource):

    #Need front implementation
    @staticmethod
    def password_check(self):
        SpecialSym = ['$', '@', '#', '%', '/']
        val = True

        if not any(char.isdigit() for char in self):
            print('Password should have at least one numeral')
            val = False

        if not any(char.isupper() for char in self):
            print('Password should have at least one uppercase letter')
            val = False

        if not any(char.islower() for char in self):
            print('Password should have at least one lowercase letter')
            val = False

        if not any(char in SpecialSym for char in self):
            print('Password should have at least one of the symbols $@#')
            val = False

        if not val:
            print("Your password is shit like my python knowledge")

        return val

    def post(self):

        if "Authorization" in request.headers.keys():
            raise Exception("405:Sorry, you can't register now. Please first logout")
        user = User(**register_schema.load(request.json))
        if session.query(User).filter(User.email == f'{user.email}').count() or \
                session.query(User).filter(User.username == f'{user.username}').count():
            raise Exception("409:User with this email or username already registered")

        session.add(user)
        session.commit()

        tokens = user.get_tokens()
        user = user.__dict__
        del user['password'], user['_sa_instance_state'], user['permission']
        tokens['user'] = user
        return jsonify(tokens), 200



class LoginApi(Resource):

    def post(self):

        if "Authorization" in request.headers.keys():
            raise Exception("405:Sorry, you can't login now. Please first logout")

        login_data = User(**login_schema.load(request.json))
        login_data.password = request.json["password"]

        user = session.query(User).filter(User.email == login_data.email).first()

        if not user:
            raise Exception('403:Wrong user email')
        if not bcrypt.verify(login_data.password, user.password):
            raise Exception('403:Wrong user password')

        tokens = user.get_tokens()
        user = user.__dict__
        del user['password'], user['_sa_instance_state'], user['permission']
        tokens['user'] = user
        return jsonify(tokens), 200


class Logout(Resource):

    # set to redis
    # jwt_redis_blocklist.set(jti, "", ex=EXPIRE)

    @jwt_required()
    def post(self):

        refresh_token = request.json.get("refresh_token")

        decoded_refresh = jwt1.decode(refresh_token, Config.SECRET_KEY, algorithms=["HS256"])
        print(decoded_refresh)
        print(decoded_refresh['sub'])

        is_refresh_revoked(jwt_payload=decoded_refresh)

        jti = decoded_refresh["jti"]
        token_type = decoded_refresh["type"]

        now = datetime.now(timezone.utc)
        session.add(TokenBlocklist(jti=jti, type=token_type, created_at=now))
        session.commit()

        return jsonify(msg=f"{token_type.capitalize()} token successfully revoked")


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

@user_info.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):

    user_info = session.query(User.email, User.username).filter(User.id == user_id).first()
    if not user_info:
        raise Exception("404:User doesn't exist")
    response = dict()

    # achievements_list = session.query(UserAchievement.achievement_id).filter(
    #     UserAchievement.user_id == user_id).all()
    #
    # if achievements_list:
    #     achievements = []
    #     for achievement_id in achievements_list:
    #         print("here")
    #         achievement = session.query(Achievement).filter(Achievement.id == achievement_id).first()
    #         achievement = achievement.__dict__
    #         del achievement['_sa_instance_state']
    #         achievements.append(achievement)
    # else:
    #     achievements = []
    # response.setdefault('user_achievements', achievements)

    response.setdefault('user_info', {"email": user_info[0],
                                      "username": user_info[1]})


    return jsonify(response), 200



@user_info.route('/profile/change/password', methods=['PUT'])
@jwt_required()
def change_password():  # check old_password
    user_id = get_jwt_identity()
    old_password = session.query(User.password).filter(User.id == user_id)
    info = request.json
    if not bcrypt.verify(info['old_password'], old_password[0][0]):
        return jsonify({"msg": "old_password is not correct"})
    session.query(User).filter(User.id == user_id).update({"password": str(bcrypt.hash(info['new_password']))})
    session.commit()
    return jsonify({"msg": "Password successfully changed"}), 200


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
user_info.add_url_rule('/registration', view_func=RegisterApi.as_view("register"))
user_info.add_url_rule('/login', view_func=LoginApi.as_view("login"))
user_info.add_url_rule('/logout', view_func=Logout.as_view("logout"))

# user_info.add_url_rule('/achievements', view_func=AchievementsBase.as_view("achievements_base"))
# user_info.add_url_rule('/achievement/<int:achievement_id>', view_func=AchievementCRUD.as_view("achievementCRUD"))

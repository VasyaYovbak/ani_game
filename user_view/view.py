from datetime import timedelta, datetime, timezone

from flask import Blueprint, request, Response, redirect, jsonify
from flask_cors import cross_origin
from flask_restful import Resource
from passlib.hash import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from http import HTTPStatus
from connection import session
from user_view.models import User, Achievement, UserAchievement, TokenBlocklist
from user_view.schema import register_schema, newAchievement, login_schema
from marshmallow import ValidationError

ACCESS_EXPIRES = timedelta(hours=1)

user_info = Blueprint('user_info', __name__)


class RegisterApi(Resource):
    def post(self):
        try:
            if "Authorization" in request.headers.keys():
                raise Exception("405:Sorry, you can't register now. Please first logout")
            user = User(**register_schema.load(request.json))
            if session.query(User).filter(User.email == f'{user.email}').count() or \
                    session.query(User).filter(User.username == f'{user.username}').count():
                raise Exception("409:User with this email or username already registered")

            session.add(user)
            session.commit()
            token = user.get_token()
            user = user.__dict__
            del user['password'], user['_sa_instance_state'], user['permission']
            return jsonify({'access_token': token,
                            'user': user
                            }), 200

        except ValidationError as e:
            return e.__dict__.get("messages"), 400
        except Exception as e:
            code, text = str(e).split(":")
            return f"Unsuccessful operation \n {text}", int(code)


class LoginApi(Resource):
    def post(self):
        try:
            if "Authorization" in request.headers.keys():
                raise Exception("405:Sorry, you can't register now. Please first logout")

            login_data = User(**login_schema.load(request.json))
            login_data.password = request.json["password"]

            user = session.query(User).filter(User.email == login_data.email).first()

            if not user:
                raise Exception('403:Wrong user email')
            if not bcrypt.verify(login_data.password, user.password):
                raise Exception('403:Wrong user password')

            token = user.get_token()
            user = user.__dict__
            del user['password'], user['_sa_instance_state'], user['permission']
            return jsonify({'access_token': token,
                            'user': user
                            }), 200
        except ValidationError as e:
            return e.__dict__.get("messages"), 400
        except Exception as e:
            code, text = str(e).split(":")
            return f"Unsuccessful operation \n {text}", int(code)


class Logout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        print(get_jwt())
        now = datetime.now(timezone.utc)
        session.add(TokenBlocklist(jti=jti, created_at=now))
        session.commit()
        return jsonify(msg="JWT revoked"), 200


class AchievementsBase(Resource):
    def get(self):
        try:
            result = []
            achievements = session.query(Achievement).all()
            if not achievements:
                raise Exception(f'400:Got problem with taking Achievements (Achievement table is empty)')
            for achievement in achievements:
                achievement = achievement.__dict__
                del achievement['_sa_instance_state']
                result.append(achievement)
            return jsonify(result), 200
        except Exception as e:
            code, text = str(e).split(":")
            return f"Unsuccessful operation \n {text}", int(code)

    @jwt_required()
    def post(self):
        try:
            permission = session.query(User.permission).filter(User.id == get_jwt_identity()).first()
            if permission[0] != 'admin':
                raise Exception("403:You dont have permissions to make this operation")
            achievements = request.json
            for achievement in achievements:
                table_achievement = Achievement(**newAchievement.load(achievement))
                if not session.query(Achievement).filter(Achievement.name == table_achievement.name).all():
                    session.add(table_achievement)
                else:
                    raise Exception(f'409:{table_achievement.name} already exists')
            session.commit()
            return "All Achievement successfully added ", 200
        except ValidationError as e:
            return jsonify(e.__dict__.get("messages")), 400
        except Exception as e:
            code, text = str(e).split(":")
            return f"Unsuccessful operation \n {text}", int(code)


class AchievementCRUD(Resource):
    def get(self, achievement_id):
        try:
            achievement = session.query(Achievement).get(achievement_id)
            if not achievement:
                raise Exception("400:Sorry , this Achievement doesn't exists")
            achievement = achievement.__dict__
            del achievement['_sa_instance_state']
            return jsonify(achievement), 200
        except Exception as e:
            code, text = str(e).split(":")
            return f"Unsuccessful operation \n {text}", int(code)

    @jwt_required()
    def put(self, achievement_id):
        try:
            permission = session.query(User.permission).filter(User.id == get_jwt_identity()).first()
            if permission[0] != 'admin':
                raise Exception("403:You dont have permissions to make this operation")
            achievement = session.query(Achievement).get(achievement_id)
            if not achievement:
                raise Exception("404:Wrong Achievement id (Achievement doesn't exist)")
            new_achievement = Achievement(**newAchievement.load(request.json))
            achievement.name = new_achievement.name
            achievement.description = new_achievement.description
            achievement.experience = new_achievement.experience
            session.commit()
            return "Achievement successfully changed ", 200

        except ValidationError as e:
            return jsonify(e.__dict__.get("messages")), 400
        except Exception as e:
            code, text = str(e).split(":")
            return f"Unsuccessful operation \n {text}", int(code)

    @jwt_required()
    def delete(self, achievement_id):
        try:
            permission = session.query(User.permission).filter(User.id == get_jwt_identity()).first()
            if permission[0] != 'admin':
                raise Exception("403:You dont have permissions to make this operation")
            achievement = session.query(Achievement).get(achievement_id)
            if not achievement:
                raise Exception("404:Wrong Achievement id (Achievement doesn't exist)")

            user_achievements = session.query(UserAchievement).filter(
                UserAchievement.achievement_id == achievement_id).all()
            for user_achievement in user_achievements:
                session.delete(user_achievement)
            session.commit()

            session.query(Achievement).filter(Achievement.id == achievement_id).delete()
            session.commit()
            return "Achievement successfully deleted", 200
        except Exception as e:
            code, text = str(e).split(":")
            return f"Unsuccessful operation \n {text}", int(code)


@user_info.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    try:
        user_info = session.query(User.email, User.username).filter(User.id == user_id).first()
        if not user_info:
            raise Exception("404:User doesn't exist")
        response = dict()

        achievements_list = session.query(UserAchievement.achievement_id).filter(
            UserAchievement.user_id == user_id).all()

        if achievements_list:
            achievements = []
            for achievement_id in achievements_list:
                print("here")
                achievement = session.query(Achievement).filter(Achievement.id == achievement_id).first()
                achievement = achievement.__dict__
                del achievement['_sa_instance_state']
                achievements.append(achievement)
        else:
            achievements = []

        response.setdefault('user_info', {"email": user_info[0],
                                          "username": user_info[1]})

        response.setdefault('user_achievements', achievements)

        return jsonify(response), 200

    except Exception as e:
        print(e)
        code, text = str(e).split(":")
        return f"Unsuccessful operation \n {text}", int(code)


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


user_info.add_url_rule('/registration', view_func=RegisterApi.as_view("register"))
user_info.add_url_rule('/login', view_func=LoginApi.as_view("login"))
user_info.add_url_rule('/logout', view_func=Logout.as_view("logout"))

user_info.add_url_rule('/achievements', view_func=AchievementsBase.as_view("achievements_base"))
user_info.add_url_rule('/achievement/<int:achievement_id>', view_func=AchievementCRUD.as_view("achievementCRUD"))

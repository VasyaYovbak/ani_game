from datetime import timedelta

from flask import Blueprint, request, Response, redirect, jsonify
from flask_cors import cross_origin
from flask_restful import Resource
from passlib.hash import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from http import HTTPStatus
from connection import session
from user_view.models import User, Achievement, UserAchievement
from user_view.schema import register_schema, newAchievement
from marshmallow import ValidationError

ACCESS_EXPIRES = timedelta(hours=1)

user_info = Blueprint('user_info', __name__)


class RegisterApi(Resource):
    def get(self):
        return redirect("/users/registunininnpration")

    def post(self):
        try:
            user = User(**register_schema.load(request.json))
            if session.query(User).filter(User.email == f'{user.email}').count() or \
                    session.query(User).filter(User.username == f'{user.username}').count():
                return Response("this user already registered", status=HTTPStatus.BAD_REQUEST)

            session.add(user)
            session.commit()
            token = user.get_token()
            return Response(str({'access_token': token}), status=HTTPStatus.OK)

        except ValidationError as e:
            return e.__dict__.get("messages")


class LoginApi(Resource):
    def post(self):
        user = session.query(User).filter(User.email == request.json['email']).one()
        if not bcrypt.verify(request.json['password'], user.password):
            raise Exception('Wrong user password')
        token = user.get_token()
        return Response(str({'access_token': token}), status=HTTPStatus.OK)


class AchievementsBase(Resource):
    def get(self):
        result = []
        achievements = session.query(Achievement).all()
        for achievement in achievements:
            achievement = achievement.__dict__
            del achievement['_sa_instance_state']
            result.append(achievement)
        return str(result)

    @jwt_required()
    def post(self):
        achievements = request.json
        for achievement in achievements:
            table_achievement = Achievement(**newAchievement.load(achievement))
            session.add(table_achievement)
        session.commit()
        return Response("All Achievement successfully added ", status=HTTPStatus.OK)


class AchievementCRUD(Resource):
    def get(self, achievement_id):

        achievement = session.query(Achievement).get(achievement_id)
        if not achievement:
            return Response("Wrong Achievement id", status=HTTPStatus.BAD_REQUEST)
        achievement = achievement.__dict__
        del achievement['_sa_instance_state']
        return Response(str(achievement), status=HTTPStatus.OK)

    def put(self, achievement_id):
        achievement = session.query(Achievement).get(achievement_id)
        if not achievement:
            return Response("Wrong Achievement id", status=HTTPStatus.BAD_REQUEST)

        new_achievement = Achievement(**newAchievement.load(request.json))

        achievement.name = new_achievement.name
        achievement.description = new_achievement.description
        achievement.experience = new_achievement.experience

        session.commit()

        return Response("Achievement successfully changed ", status=HTTPStatus.OK)

    def delete(self, achievement_id):
        achievement = session.query(Achievement).get(achievement_id)
        if not achievement:
            return Response("Wrong Achievement id", status=HTTPStatus.BAD_REQUEST)

        user_achievements = session.query(UserAchievement).filter(UserAchievement.achievement_id == achievement_id).all()
        for user_achievement in user_achievements:
            session.delete(user_achievement)
        session.commit()

        session.query(Achievement).filter(Achievement.id == achievement_id).delete()
        session.commit()
        return Response("Achievement successfully deleted", status=HTTPStatus.OK)


@user_info.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    achievement = AchievementsBase()
    achievements = achievement.get()
    user_info = session.query(User.email, User.username).filter(User.id == user_id)

    response = dict()
    response.setdefault('user_info', user_info[0])
    response.setdefault('user_achievements', achievements)

    return str(response), 200


@user_info.route('/profile/change/password', methods=['PUT'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    new_password = request.json['password']
    session.query(User).filter(User.id == user_id).update({"password": str(bcrypt.hash(new_password))})
    session.commit()
    return "Password successfully changed", 200


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

user_info.add_url_rule('/achievements', view_func=AchievementsBase.as_view("achievements_base"))
user_info.add_url_rule('/achievement/<int:achievement_id>', view_func=AchievementCRUD.as_view("achievementCRUD"))

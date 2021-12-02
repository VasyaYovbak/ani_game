# from http import HTTPStatus
#
# from flask import Response, request, Blueprint
# from flask_restful import Resource
# from sqlalchemy.orm import Session
#
# from character_view.models import Character
# from game_view.models import Game, Card
# from user_view.models import User, Achievement, UserAchievement
# from connection import engine
#
# from user_view.models import User
#
# database_test = Blueprint('database_test', __name__)
# session = Session(bind=engine)
#
#
# class TestDatabase(Resource):
#     def post(self):
#         for i in request.json:
#             if i == "new_users":
#                 users = request.json["new_users"]
#                 for user in users:
#                     table_user = User(**user)
#                     session.add(table_user)
#             if i == "new_achievements":
#                 achievements = request.json["new_achievements"]
#                 for achievement in achievements:
#                     table_achievement = Achievement(**achievement)
#                     session.add(table_achievement)
#             if i == "new_characters":
#                 characters = request.json["new_characters"]
#                 for character in characters:
#                     table_character = Character(**character)
#                     session.add(table_character)
#             if i == "new_user_achievements":
#                 user_achievements = request.json["new_user_achievements"]
#                 for user_achievement in user_achievements:
#                     table_user_achievement = UserAchievement(**user_achievement)
#                     session.add(table_user_achievement)
#             if i == "new_games":
#                 games = request.json["new_games"]
#                 for game in games:
#                     table_game = Game(**game)
#                     session.add(table_game)
#             if i == "new_cards":
#                 cards = request.json["new_cards"]
#                 for card in cards:
#                     table_card = Card(**card)
#                     session.add(table_card)
#
#         session.commit()
#         session.close()
#         return Response(status=HTTPStatus.OK)
#
#
# database_test.add_url_rule("/database/tests", view_func=TestDatabase.as_view("datatest"))

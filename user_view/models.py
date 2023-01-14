import datetime

from sqlalchemy import Table, Integer, String, \
    Column, ForeignKey, Boolean, DateTime, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from passlib.hash import argon2
from passlib.hash import bcrypt_sha256
from base import Base


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False)
    confirmed = Column(Boolean, nullable=False, default=False)
    confirmed_on = Column(DateTime, nullable=True)
    permission = Column(String(30))
    rating = Column(Integer(), nullable=True)
    password = Column(String(100), nullable=False)
    image = Column(String(200), nullable=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = argon2.using(rounds=5, ).hash(password)
        self.permission = 'user'
        self.rating = 0

    access_expire_time = timedelta(minutes=3)
    refresh_expire_time = timedelta(hours=12)
    reset_expire_time = timedelta(minutes=30)
    verify_expire_time = timedelta(minutes=30)

    def get_access_token(self, access_expire_time):
        expire_delta = access_expire_time
        access_token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return access_token

    def get_refresh_token(self, refresh_expire_time):
        expire_delta = refresh_expire_time
        refresh_token = create_refresh_token(
            identity=self.id, expires_delta=expire_delta)
        return refresh_token

    def generate_reset_token(self, reset_expire_time):
        expire_delta = reset_expire_time
        reset_token = create_refresh_token(
            identity=self.id, expires_delta=expire_delta)
        return reset_token

    def generate_verify_token(self, verify_expire_time):
        expire_delta = verify_expire_time
        verify_token = create_refresh_token(
            identity=self.id, expires_delta=expire_delta)
        return verify_token

    def get_tokens(self):

        access = self.get_access_token(self.access_expire_time)
        refresh = self.get_refresh_token(self.refresh_expire_time)

        return {'access_token': access, 'refresh_token': refresh}

    def get_reset_token(self):

        reset = self.generate_reset_token(self.reset_expire_time)
        return reset

    def get_verify_token(self):

        verify = self.generate_verify_token(self.verify_expire_time)
        return verify


class TokenBlocklist(Base):

    __tablename__ = 'token_block_list'

    id = Column(Integer(), primary_key=True)
    jti = Column(String(36), nullable=False)
    type = Column(String(16), nullable=False)
    created_at = Column(DateTime(), nullable=False)

# User Achievements
# class Achievement(Base):
#     __tablename__ = 'achievement'
#     id = Column(Integer(), primary_key=True, autoincrement=True)
#     name = Column(String(30), nullable=False)
#     experience = Column(Integer(), nullable=False)
#     description = Column(String(120), nullable=False)
#
#
# class UserAchievement(Base):
#     __tablename__ = 'user_achievement'
#     user_id = Column(Integer(), ForeignKey('user.id'), primary_key=True)
#     achievement_id = Column(Integer(), ForeignKey('achievement.id'), primary_key=True)
#
#     user = relationship("User")
#     achievement = relationship("Achievement")

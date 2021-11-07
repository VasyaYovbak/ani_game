import datetime

from sqlalchemy import Table, Integer, String, \
    Column, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt

from base import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False)
    permission = Column(String(30))
    rating = Column(Integer(), nullable=False)
    password = Column(String(100), nullable=False)
    image = Column(String(200), nullable=True)

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))
        self.permission = 'user'
        self.rating = 0

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token


class Achievement(Base):
    __tablename__ = 'achievement'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    experience = Column(Integer(), nullable=False)
    description = Column(String(120), nullable=False)


class UserAchievement(Base):
    __tablename__ = 'user_achievement'
    user_id = Column(Integer(), ForeignKey('user.id'), primary_key=True)
    achievement_id = Column(Integer(), ForeignKey('achievement.id'), primary_key=True)

    user = relationship("User")
    achievement = relationship("Achievement")

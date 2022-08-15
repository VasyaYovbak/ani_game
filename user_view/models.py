import datetime

from sqlalchemy import Table, Integer, String, \
    Column, ForeignKey, Boolean, DateTime, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from flask_jwt_extended import create_access_token, create_refresh_token
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

    def get_access_token(self, expire_time=1):
        expire_delta = timedelta(expire_time)
        access_token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return access_token

    def get_refresh_token(self, expire_time=1):
        expire_delta = timedelta(expire_time)
        refresh_token = create_refresh_token(
            identity=self.id, expires_delta=expire_delta)
        return refresh_token

    def get_tokens(self):

        access = self.get_access_token()
        refresh = self.get_refresh_token()

        return {'access_token': access, 'refresh_token': refresh}


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


class TokenBlocklist(Base):

    __tablename__ = 'token_block_list'

    id = Column(Integer(), primary_key=True)
    jti = Column(String(36), nullable=False)
    type = Column(String(16), nullable=False)
    created_at = Column(DateTime(), nullable=False)


session_maker = sessionmaker(bind=create_engine('mysql+mysqldb://root:MyZno26112003@localhost/anigame'))

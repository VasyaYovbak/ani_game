from sqlalchemy import Integer, String, \
    Column, ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class Character(Base):
    __tablename__ = 'character'
    character_id = Column(Integer(), primary_key=True)
    name = Column(String(40), nullable=False)
    image = Column(String(250), nullable=False)
    anime_id = Column(Integer, ForeignKey('anime.anime_id'))

    anime_relation = relationship("Anime", primaryjoin="Character.anime_id==Anime.anime_id")


class Anime(Base):
    __tablename__ = 'anime'
    anime_id = Column(Integer(), primary_key=True)
    name = Column(String(40), nullable=False)
    image = Column(String(250), nullable=False)

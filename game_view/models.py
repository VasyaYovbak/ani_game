from sqlalchemy import Integer, String, \
    Column, DateTime, ForeignKey, Boolean, Time
from sqlalchemy.orm import relationship

from base import Base


class Game(Base):
    __tablename__ = 'game'
    game_id = Column(Integer(), primary_key=True)
    guested_character_id = Column(Integer, ForeignKey('character.character_id'))
    unguested_character_id = Column(Integer, ForeignKey('character.character_id'))
    winner_id = Column(Integer, ForeignKey('user.id'))
    loser_id = Column(Integer, ForeignKey('user.id'))
    date = Column(DateTime)
    chat = Column(String(1000))

    guested_relation = relationship("Character", primaryjoin="Game.guested_character_id==Character.character_id")
    winner_relation = relationship("User", primaryjoin="Game.winner_id==User.id")


class Card(Base):
    __tablename__ = 'card'
    card_id = Column(Integer(), primary_key=True)
    character_id = Column(Integer, ForeignKey('character.character_id'))
    is_active = Column(Boolean(), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    is_selected_hero = Column(Boolean(), nullable=False)
    game_id = Column(Integer, ForeignKey('game.game_id'))

    character = relationship("Character", primaryjoin="Card.character_id==Character.character_id")
    user = relationship("User", primaryjoin="Card.user_id==User.id")
    game = relationship("Game", primaryjoin="Card.game_id==Game.game_id")


class UserQueue(Base):
    __tablename__ = 'user_queue'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    rating = Column(Integer(), nullable=False)

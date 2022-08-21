from sqlalchemy import Integer, String, \
    Column, DateTime, ForeignKey, Boolean, Time, PrimaryKeyConstraint
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


class GameRoom(Base):
    __tablename__ = 'game_room'
    room_id = Column(Integer(), primary_key=True)
    name = Column(String(40), nullable=False)
    creator_user_id = Column(Integer, ForeignKey('user.id'))
    second_user_id = Column(Integer, ForeignKey('user.id'))
    is_game_started = Column(Boolean())

    creator_relation = relationship("User", primaryjoin="GameRoom.creator_user_id==User.id")
    second_user_relation = relationship("User", primaryjoin="GameRoom.second_user_id==User.id")


class GamesAnimeList(Base):
    __tablename__ = 'games_anime_list'
    game_id = Column(Integer, ForeignKey('game.game_id'))
    anime_id = Column(Integer, ForeignKey('anime.anime_id'))

    game_relation = relationship("Game", primaryjoin="GamesAnimeList.game_id==Game.game_id")
    anime_relation = relationship("Anime", primaryjoin="GamesAnimeList.anime_id==Anime.anime_id")
    __table_args__ = (
        PrimaryKeyConstraint('game_id', 'anime_id', name='pk_id'),
    )


class RoomsAnimeList(Base):
    __tablename__ = 'rooms_anime_list'
    room_id = Column(Integer, ForeignKey('game_room.room_id'))
    anime_id = Column(Integer, ForeignKey('anime.anime_id'))

    room_relation = relationship("GameRoom", primaryjoin="RoomsAnimeList.room_id==GameRoom.room_id")
    anime_relation = relationship("Anime", primaryjoin="RoomsAnimeList.anime_id==Anime.anime_id")
    __table_args__ = (
        PrimaryKeyConstraint('room_id', 'anime_id', name='pk_id'),
    )

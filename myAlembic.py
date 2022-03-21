from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKeyConstraint, DateTime, Time, \
    Boolean
from connection import engine

meta = MetaData()
Table('achievement', meta,
      Column('id', Integer(), autoincrement=True, nullable=False, primary_key=True),
      Column('name', String(length=30), nullable=False),
      Column('experience', Integer(), nullable=False),
      Column('description', String(length=120), nullable=False),
      )
Table('character', meta,
      Column('character_id', Integer(), nullable=False, primary_key=True),
      Column('name', String(length=40), nullable=False),
      Column('image', String(length=250), nullable=False),
      )
Table('token_block_list', meta,
      Column('id', Integer(), nullable=False, primary_key=True),
      Column('jti', String(length=36), nullable=False),
      Column('created_at', DateTime(), nullable=False),
      )
Table('user', meta,
      Column('id', Integer(), nullable=False, primary_key=True),
      Column('username', String(length=50), nullable=False),
      Column('email', String(length=200), nullable=False),
      Column('permission', String(length=30), nullable=True),
      Column('rating', Integer(), nullable=False),
      Column('password', String(length=100), nullable=False),
      Column('image', String(length=200), nullable=True),
      )
Table('game', meta,
      Column('game_id', Integer(), nullable=False, primary_key=True),
      Column('guested_character_id', Integer(), nullable=True),
      Column('unguested_character_id', Integer(), nullable=True),
      Column('winner_id', Integer(), nullable=True),
      Column('loser_id', Integer(), nullable=True),
      Column('date', DateTime(), nullable=True),
      Column('duration', Time(), nullable=True),
      Column('chat', String(length=1000), nullable=True),
      ForeignKeyConstraint(['guested_character_id'], ['character.character_id']),
      ForeignKeyConstraint(['loser_id'], ['user.id'], ),
      ForeignKeyConstraint(['unguested_character_id'], ['character.character_id'], ),
      ForeignKeyConstraint(['winner_id'], ['user.id'], ),
      )
Table('user_achievement', meta,
      Column('user_id', Integer(), nullable=False, primary_key=True),
      Column('achievement_id', Integer(), nullable=False, primary_key=True),
      ForeignKeyConstraint(['achievement_id'], ['achievement.id'], ),
      ForeignKeyConstraint(['user_id'], ['user.id'], ),
      )
Table('user_queue', meta,
      Column('user_id', Integer(), nullable=False, primary_key=True),
      Column('rating', Integer(), nullable=False),
      ForeignKeyConstraint(['user_id'], ['user.id'], ),
      )
Table('card', meta,
      Column('card_id', Integer(), nullable=False, primary_key=True),
      Column('character_id', Integer(), nullable=True),
      Column('is_active', Boolean(), nullable=False),
      Column('user_id', Integer(), nullable=True),
      Column('is_selected_hero', Boolean(), nullable=False),
      Column('game_id', Integer(), nullable=True),
      ForeignKeyConstraint(['character_id'], ['character.character_id'], ),
      ForeignKeyConstraint(['game_id'], ['game.game_id'], ),
      ForeignKeyConstraint(['user_id'], ['user.id'], ),
      )
meta.create_all(engine)

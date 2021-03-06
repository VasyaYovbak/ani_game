from sqlalchemy import Integer, String, \
    Column, DateTime, ForeignKey, Boolean, Time
from base import Base


class Character(Base):
    __tablename__ = 'character'
    character_id = Column(Integer(), primary_key=True)
    name = Column(String(40), nullable=False)
    image = Column(String(250), nullable=False)

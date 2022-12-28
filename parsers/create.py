from character_view.models import Anime, Character
from connection import engine

Anime.__table__.create(engine)
Character.__table__.create(engine)

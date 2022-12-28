from character_view.models import Character, Anime
from connection import session
from parsers.functions.mapper import anime_character_foreign_keys


def download_anime(session, name, image_url):
    anime_id = anime_character_foreign_keys[name]
    anime = Anime(anime_id=anime_id, name=name,
                  image=image_url)
    session.add(anime)
    session.commit()


def download_characters(session, df):
    for i, row in df.iterrows():
        character = Character(**row)
        session.add(character)
    session.commit()

    # # Read data you added to database
    # # print([q.__dict__ for q in session.query(Character).all()])


def print_particular_anime_characters(anime_id: int) -> None:
    print([q.__dict__ for q in
           session.query(Character).filter(Character.anime_id == anime_id).all()])

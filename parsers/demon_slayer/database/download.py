from connection import session
from parsers.functions.convert import prepare_characters_dataframe
from parsers.functions.create_collage import get_one_row_image_coordinates
from parsers.functions.download import download_anime, download_characters, print_particular_anime_characters
from parsers.functions.mapper import anime_character_foreign_keys, one_image_size_usual
from parsers.functions.setup import *

df = pd.read_csv('../data/demon_slayer.txt')
number_of_img = len(df.index) - 1

df = prepare_characters_dataframe(df=df, columns_to_drop=['image'], columns_rename_mapper={
    'full_name': 'name'},
                                  anime_foreign_key=anime_character_foreign_keys['demon_slayer'])

dragon_ball_characters_df = df.assign(
    image=get_one_row_image_coordinates(number_of_img, one_image_size_usual))


# print(dragon_ball_characters_df)


def download_demon_slayer_data(session):
    download_anime(session=session, name='demon_slayer',
                   image_url="https://assets.stickpng.com/images/5ede49f9b760540004f2c5e7.png")
    download_characters(session=session, df=dragon_ball_characters_df)

# # download only demon slayer data
# download_demon_slayer_data(session=session)

# print_particular_anime_characters(anime_character_foreign_keys['demon_slayer'])

from parsers.functions.convert import prepare_characters_dataframe
from parsers.functions.create_collage import get_one_row_image_coordinates
from parsers.functions.download import download_anime, download_characters, print_particular_anime_characters
from parsers.functions.mapper import anime_character_foreign_keys, one_image_size_usual
from parsers.functions.setup import *

import os

df = pd.read_csv(os.path.dirname(__file__) + '\\..\data\\dragon_ball.txt')
number_of_img = len(df.index) - 1

df = prepare_characters_dataframe(df=df, columns_to_drop=['image'], columns_rename_mapper={
    'full_name': 'name'},
                                  anime_foreign_key=anime_character_foreign_keys['dragon_ball'])

dragon_ball_characters_df = df.assign(
    image=get_one_row_image_coordinates(number_of_img, one_image_size_usual))


def download_dragon_ball_data(session):
    download_anime(session=session, name='dragon_ball',
                   image_url="https://www.pngall.com/wp-content/uploads/12/Dragon-Ball-Z-Series-PNG-Images.png")
    download_characters(session=session, df=dragon_ball_characters_df)

# # download only dragon ball data
# download_dragon_ball_data(session=session)

# print_particular_anime_characters(anime_character_foreign_keys['dragon_ball'])

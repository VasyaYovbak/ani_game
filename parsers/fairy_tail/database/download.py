from connection import session
from parsers.functions.convert import prepare_characters_dataframe
from parsers.functions.create_collage import get_one_row_image_coordinates
from parsers.functions.download import download_anime, download_characters, print_particular_anime_characters
from parsers.functions.mapper import anime_character_foreign_keys, one_image_size_usual
from parsers.functions.setup import *

import os

df = pd.read_csv(os.path.dirname(__file__) + '\\..\data\\fairy_tail.txt')
number_of_img = len(df.index) - 1

df = prepare_characters_dataframe(df=df, columns_to_drop=['image'], columns_rename_mapper={
    'full_name': 'name'},
                                  anime_foreign_key=anime_character_foreign_keys['fairy_tail'])

fairy_tail_df = df.assign(
    image=get_one_row_image_coordinates(number_of_img, one_image_size_usual))


# print(fairy_tail_df)


def download_fairy_tail_data(session):
    download_anime(session=session, name='fairy_tail',
                   image_url="https://freepikpsd.com/file/2019/10/happy-fairy-tail-png-7-Transparent-Images.png")
    download_characters(session=session, df=fairy_tail_df)

# # download only demon slayer data
# download_demon_slayer_data(session=session)

# print_particular_anime_characters(anime_character_foreign_keys['demon_slayer'])

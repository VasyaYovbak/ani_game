import os

import pandas as pd

from connection import session
from parsers.functions.convert import prepare_characters_dataframe
from parsers.functions.create_collage import get_one_row_image_coordinates
from parsers.functions.download import download_anime, download_characters, print_particular_anime_characters
from parsers.functions.mapper import anime_character_foreign_keys, one_image_size_usual

df = pd.read_csv(os.path.dirname(__file__) + '\\..\data\\filtered_by_hand.txt', sep=" ", index_col=0)
number_of_img = len(df.index) - 1

df = prepare_characters_dataframe(df=df, columns_to_drop=['image'], columns_rename_mapper={
    'full_name': 'name'},
                                  anime_foreign_key=anime_character_foreign_keys['naruto'])

naruto_characters_df = df.assign(
    image=get_one_row_image_coordinates(number_of_img, one_image_size_usual))


def download_naruto_data(session):
    download_anime(session=session, name='naruto',
                   image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZ136oXI3e_UMnW6MbHqMZ8WMU-BWzg0-WUg&usqp=CAU")
    download_characters(session=session, df=naruto_characters_df)


# # download only my hero academia data
# download_naruto_data(session=session)
#
# print_particular_anime_characters(anime_character_foreign_keys['naruto'])

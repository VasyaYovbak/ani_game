from parsers.functions.convert import prepare_characters_dataframe
from parsers.functions.download import download_anime, download_characters, print_particular_anime_characters
from parsers.functions.mapper import anime_character_foreign_keys, one_image_size_usual
from parsers.functions.setup import *

import os

df = pd.read_csv(os.path.dirname(__file__) + '\\..\data\\filtered_by_hand.txt', sep=" ")
number_of_img = len(df.index) - 1

df = prepare_characters_dataframe(df=df, columns_to_drop=['image'], columns_rename_mapper={
    'full_name': 'name'},
                                  anime_foreign_key=anime_character_foreign_keys['hunter'])

hunter_characters_df = df.assign(
    image=[f'-{str(x)}px 0' for x in range(0, number_of_img * one_image_size_usual + 1, one_image_size_usual)])


def download_hunter_data(session):
    download_anime(session=session, name='hunter',
                   image_url="https://toppng.com/public/uploads/thumbnail/in-a-fight-between-luffy-and-gon-gon-hunter-x-hunter-profile-11563215288pyzx8ubkyr.png")
    download_characters(session=session, df=hunter_characters_df)

# # download only one hunter data
# download_hunter_data(session=session)

# print_particular_anime_characters(anime_character_foreign_keys['hunter'])

from parsers.functions.convert import prepare_characters_dataframe
from parsers.functions.download import download_anime, download_characters, print_particular_anime_characters
from parsers.functions.mapper import anime_character_foreign_keys, one_image_size_usual
from parsers.functions.setup import *

import os

df = pd.read_csv(os.path.dirname(__file__) + '\\..\data\\filtered_by_hand.txt', sep=" ")
number_of_img = len(df.index) - 1
df = prepare_characters_dataframe(df=df, columns_to_drop=['id', 'image', 'appearance'], columns_rename_mapper={
    'full_name': 'name'},
                                  anime_foreign_key=anime_character_foreign_keys['one_piece'])

one_piece_characters_df = df.assign(
    image=[f'-{str(x)}px 0' for x in range(0, number_of_img * one_image_size_usual + 1, one_image_size_usual)])


def download_one_piece_data(session):
    download_anime(session=session, name='one_piece',
                   image_url="https://avatanplus.com/files/resources/original/5783d18a505e9155daea8459.png")
    download_characters(session=session, df=one_piece_characters_df)

# # download only one piece data
# download_one_piece_data(session=session)

# print_particular_anime_characters(anime_character_foreign_keys['one_piece'])

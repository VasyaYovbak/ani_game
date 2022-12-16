from parsers.functions.convert import prepare_characters_dataframe
from parsers.functions.download import download_anime, download_characters, print_particular_anime_characters
from parsers.functions.mapper import anime_character_foreign_keys, one_image_size_usual
from parsers.functions.setup import *

# preparing data

import os

df = pd.read_csv(os.path.dirname(__file__) + '\\..\data\\one_punch.txt')
number_of_img = len(df.index) - 1

df = prepare_characters_dataframe(df=df, columns_to_drop=['image'], columns_rename_mapper={'full_name': 'name'},
                                  anime_foreign_key=anime_character_foreign_keys['one_punch'])

one_punch_characters_df = df.assign(
    image=[f'-{str(x)}px 0' for x in range(0, number_of_img * one_image_size_usual + 1, one_image_size_usual)])


def download_one_punch_data(session):
    download_anime(session=session, name='one_punch',
                   image_url="https://static.wikia.nocookie.net/p__/images/2/27/Saitama.png/revision/latest?cb=20200701024620&path-prefix=protagonist")
    download_characters(session=session, df=one_punch_characters_df)

# # Download only one_punch data
# download_one_punch_data(session)

# print_particular_anime_characters(anime_character_foreign_keys['one_punch'])

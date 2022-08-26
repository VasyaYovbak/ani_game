from connection import session
from parsers.functions.convert import prepare_characters_dataframe
from parsers.functions.create_collage import get_one_row_image_coordinates
from parsers.functions.download import download_anime, download_characters, print_particular_anime_characters
from parsers.functions.mapper import anime_character_foreign_keys, one_image_size_usual
from parsers.functions.setup import *

df = pd.read_csv('../data/filtered_by_hand.txt')
number_of_img = len(df.index) - 1

df = prepare_characters_dataframe(df=df, columns_to_drop=['image'], columns_rename_mapper={
    'full_name': 'name'},
                                  anime_foreign_key=anime_character_foreign_keys['my_hero_academia'])

my_hero_academia_characters_df = df.assign(
    image=get_one_row_image_coordinates(number_of_img, one_image_size_usual))


def download_my_hero_academia_data(session):
    download_anime(session=session, name='my_hero_academia',
                   image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRKP8xSzngoIZ1fKkYSg79VnN7vE8F6HHkviw&usqp=CAU")
    download_characters(session=session, df=my_hero_academia_characters_df)


# # download only my hero academia data
# download_my_hero_academia_data(session=session)

# print_particular_anime_characters(anime_character_foreign_keys['my_hero_academia'])

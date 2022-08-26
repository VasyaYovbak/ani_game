from connection import session
from parsers.functions.convert import prepare_characters_dataframe
from parsers.functions.create_collage import get_one_row_image_coordinates
from parsers.functions.download import download_anime, download_characters, print_particular_anime_characters
from parsers.functions.mapper import anime_character_foreign_keys, one_image_size_usual
from parsers.functions.setup import *

df = pd.read_csv('../data/attack_on_titan.txt')
number_of_img = len(df.index) - 1

df = prepare_characters_dataframe(df=df, columns_to_drop=['image'], columns_rename_mapper={
    'full_name': 'name'},
                                  anime_foreign_key=anime_character_foreign_keys['attack_on_titan'])

attack_on_titan_characters_df = df.assign(
    image=get_one_row_image_coordinates(number_of_img, one_image_size_usual))


def download_attack_on_titan_data(session):
    download_anime(session=session, name='attack_on_titan',
                   image_url="https://as01.epimg.net/meristation_en/imagenes/2022/02/04/news/1643951848_207210_1643951977_noticia_normal.jpg")
    download_characters(session=session, df=attack_on_titan_characters_df)


# # download only attack on titan data
# download_attack_on_titan_data(session=session)

# print_particular_anime_characters(anime_character_foreign_keys['attack_on_titan'])

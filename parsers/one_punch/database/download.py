from parsers.functions.setup import *

# preparing data

df = pd.read_csv('../data/one_punch.txt')

df.rename(columns={'full_name': 'name'}, inplace=True)
df = df.assign(anime_id=lambda x: 2)
number_of_img = 137
one_img_size = 150

df.drop(columns=['image'], inplace=True)

df = df.assign(image_x=[x for x in range(0, number_of_img * one_img_size + 1, one_img_size)])

from parsers.functions.setup import *
from parsers.my_hero_academia.data.raw_data import my_hero_academia_data

df = pd.DataFrame(my_hero_academia_data)

df.to_csv('../data/my_hero_academia_data.txt', index=False, header=['full_name', 'image'])

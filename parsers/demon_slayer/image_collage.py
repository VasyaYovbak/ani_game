from parsers.functions.setup import *
from parsers.functions.create_collage import create_one_row_collage


df = pd.read_csv('./data/demon_slayer.txt', sep=",")
# print(df)

collage = create_one_row_collage(df)
collage.save('collage.jpg')

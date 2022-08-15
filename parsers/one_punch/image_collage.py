from parsers.functions.create_collage import create_one_row_collage
from parsers.functions.setup import *
df = pd.read_csv('data/one_punch.txt')

collage = create_one_row_collage(df)

collage.save('collage.jpg')

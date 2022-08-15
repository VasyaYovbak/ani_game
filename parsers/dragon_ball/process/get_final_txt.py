from parsers.dragon_ball.data.raw_data import data
from parsers.functions.setup import *

df = pd.DataFrame(data)
df.drop(df.columns[2], inplace=True, axis=1)

df.to_csv('../data/dragon_ball.txt', index=False)

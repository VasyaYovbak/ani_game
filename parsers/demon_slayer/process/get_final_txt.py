from parsers.demon_slayer.data.raw_data import data
from parsers.functions.setup import *

df = pd.DataFrame(data)

df.drop(df.columns[2], inplace=True, axis=1)
# print(df)
df.to_csv('../data/demon_slayer.txt', index=False)

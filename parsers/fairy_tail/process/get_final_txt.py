from parsers.fairy_tail.data.raw_data import fairy_tail_data
from parsers.functions.setup import *

df = pd.DataFrame(fairy_tail_data)

df.drop(df.columns[2], inplace=True, axis=1)
# print(df)
df.to_csv('../data/fairy_tail.txt', index=False)

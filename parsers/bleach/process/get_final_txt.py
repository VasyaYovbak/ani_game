from parsers.bleach.data.raw_data import bleach_data
from parsers.functions.setup import *

df = pd.DataFrame(bleach_data)
# df.drop(df.columns[2], inplace=True, axis=1)
# print(df)
df.to_csv('../data/bleach.txt', index=False)

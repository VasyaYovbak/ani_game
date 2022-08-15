from parsers.functions.setup import *

# # writing raw data to txt
from parsers.one_punch.data.raw_data import one_punch_characters_data

df = pd.DataFrame(one_punch_characters_data)
df.to_csv('../data/one_punch.txt', index=False)

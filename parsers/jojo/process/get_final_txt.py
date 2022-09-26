from parsers.functions.setup import *

# # writing raw data to txt
from parsers.jojo.data.raw_data import data

df = pd.DataFrame(data)
df.to_csv('../data/jojo.txt', index=False)

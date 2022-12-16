from parsers.attack_on_titan.data.raw_data import attack_on_titan_data
from parsers.functions.setup import *

df = pd.DataFrame(attack_on_titan_data)
df.drop(df.columns[2], inplace=True, axis=1)

df.to_csv('../data/attack_on_titan.txt', index=False)

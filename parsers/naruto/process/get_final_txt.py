import pandas as pd

from parsers.naruto.data.raw_data import parsed_naruto_characters

df = pd.DataFrame(parsed_naruto_characters)
df.to_csv('../data/naruto_data.txt', sep=" ")

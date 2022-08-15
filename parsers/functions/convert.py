import pandas as pd
from io import BytesIO


def by_hand_txt_to_final_data_txt(by_hand_path: str, final_path: str, columns_to_drop: list, sep=' ', out_index=True):
    pd.set_option('display.width', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', None)

    df = pd.read_csv(by_hand_path, sep=" ", header=None)
    df.drop(df.columns[columns_to_drop], inplace=True, axis=1)
    print(df)

    df.to_csv(final_path, sep=sep, mode='a', header=None, index=out_index)


def convert_img_to_format(im, desired_format):
    with BytesIO() as f:
        im.save(f, format=desired_format)
        return f.getvalue()

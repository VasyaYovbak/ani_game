from typing import List, Dict

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


def prepare_characters_dataframe(df, columns_to_drop: List[str], anime_foreign_key: int,
                                 columns_rename_mapper: Dict[str, str]):
    """Rename drop and assign column in the same time.
    :return DateFrame
    """

    df = df.drop(columns=columns_to_drop)
    df = df.rename(columns=columns_rename_mapper)
    df = df.assign(anime_id=lambda x: anime_foreign_key)
    return df

from collections import defaultdict
from typing import List, Dict


def merge_dicts(lst_of_dicts: List[Dict], keys_to_merge: List[str]) -> dict:
    res = defaultdict(list)
    for dictionary in lst_of_dicts:
        for key in keys_to_merge:
            res[key] += dictionary[key]
    return res

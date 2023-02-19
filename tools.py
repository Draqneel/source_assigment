import json

from pathlib import Path


def json_to_dict(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def row_data_to_dict(keys: tuple, fetch_data) -> dict:
    result = {}
    for row in fetch_data:
        tmp = dict(zip(keys, row))
        result[tmp['dttm']] = tmp

    return result

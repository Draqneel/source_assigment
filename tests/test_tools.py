import os
import unittest

from pathlib import Path
from tools import json_to_dict, row_data_to_dict


class Testing(unittest.TestCase):
    def test_json_to_dict(self):
        test_path = Path(os.path.dirname(os.path.realpath(__file__))).resolve() / 'mock_data' / 'test.json'
        expected_res = {
            "key_example": "value_example"
        }
        res = json_to_dict(test_path)
        self.assertEqual(res, expected_res)

    def test_row_data_to_dict(self):
        _fetch_data_test = [("val1", "val2", "val3", "01.01.2023")]
        _keys = ("key1", "key2", "key3", "dttm")
        expected_res = {
            "01.01.2023": {
                "dttm": "01.01.2023",
                "key1": "val1",
                "key2": "val2",
                "key3": "val3",
            }
        }
        res = row_data_to_dict(_keys, _fetch_data_test)
        self.assertEqual(res, expected_res)
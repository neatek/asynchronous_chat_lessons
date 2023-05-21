import sys
import os
import unittest
import json
from datetime import datetime

sys.path.append(os.path.join(os.getcwd(), "lesson4"))
print(os.path.join(os.getcwd()))
from functions.func_server import read_package


class TestClass(unittest.TestCase):
    def test_for_KeyError(self):
        self.assertRaises(
            KeyError,
            read_package,
            '{"somedata": "data"}'.encode(),
        )

    # AssertionError: KeyError not raised by read_package
    def test_for_KeyError_2(self):
        self.assertRaises(
            KeyError,
            read_package,
            '{"somedata": "data","action":"1"}'.encode(),
        )

    # AssertionError: <class 'dict'> != <class 'str'>
    def test_value_type(self):
        self.assertEqual(
            type(read_package('{"somedata": "data","action":"test"}'.encode())),
            type("str"),
        )


if __name__ == "__main__":
    unittest.main()

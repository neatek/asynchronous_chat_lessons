import sys
import os
import unittest
import json
from datetime import datetime

sys.path.append(os.path.join(os.getcwd(), "lesson4"))
print(os.path.join(os.getcwd()))
from functions.func_client import message


class TestClass(unittest.TestCase):
    # AssertionError: b'{"action": "action", "message": "message", "time": 1682034662.340103}' != {'action': 'action', 'message': 'message', 'time': 1682034662.341103}
    def test_main(self):
        self.assertEqual(
            message("action", "message"),
            json.dumps(
                {
                    "action": "action",
                    "message": "message",
                    "time": datetime.now().timestamp(),
                }
            ).encode(),
        )

    def test_action(self):
        # AssertionError: 'action' != 'exit'
        self.assertEqual(
            json.loads(message("action", "message").decode("utf-8"))["action"], "exit"
        )

    def test_for_test(self):
        # AssertionError: ValueError not raised by message
        self.assertRaises(
            ValueError,
            message,
            "exit",
        )


if __name__ == "__main__":
    unittest.main()

import json
from datetime import datetime


def message(response: int = 200, message: str = ""):
    message = json.dumps(
        {
            "response": response,
            "message": message,
            "time": datetime.now().timestamp(),
        }
    )
    return message.encode()


def read_package(data: bytes):
    if bytes:
        data = json.loads(data.decode("utf-8"))

        if data["action"] == "quit":
            print(f"Close connection socket")

    return data

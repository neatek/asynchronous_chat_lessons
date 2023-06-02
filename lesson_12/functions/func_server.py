import json
from datetime import datetime
from log.server_log_config import logger


class ActionMissing(Exception):
    def __str__(self):
        return "Action is missing"


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
    try:
        decoded = data.decode("utf-8")
        if bytes:
            try:
                data = json.loads(decoded)
            except BaseException as e:
                print(str(e))
                return None
    except KeyError:
        raise ActionMissing()
    return data

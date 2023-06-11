import json
from datetime import datetime
from log.client_log_config import logger


def message(action: str = "", message: str = ""):
    data = {
        "action": action,
        "message": message,
        "time": datetime.now().timestamp(),
    }
    return json.dumps(data).encode()

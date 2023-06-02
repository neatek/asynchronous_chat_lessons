import json
from datetime import datetime
from log.client_log_config import logger
import dataclasses as dc


@dc.dataclass(eq=True)
class MessageFormat:
    action: str
    message: str
    receiver: str
    sender: str


def message(data: MessageFormat):
    data = {
        "action": data.action,
        "receiver": data.receiver,
        "sender": data.sender,
        "message": data.message,
        "time": datetime.now().timestamp(),
    }
    return json.dumps(data).encode()

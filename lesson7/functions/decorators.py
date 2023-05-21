import sys
import logging
import traceback
from datetime import datetime

if sys.argv[0].find("client.py") == -1:
    logger = logging.getLogger("server")
else:
    logger = logging.getLogger("client")


def log(logging_function):
    def log_saver(*args, **kwargs):
        result = logging_function(*args, **kwargs)
        logger.debug(
            f"[{datetime.now()}] Функция {logging_function.__name__} вызвана из функции {traceback.format_stack()[0].strip().split()[-1]}. (Параметры: {args}, {kwargs})"
        )
        return result

    return log_saver


if __name__ == "__main__":
    print(sys.argv[0])

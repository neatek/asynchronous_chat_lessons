import sys
import os
import logging
import logging.handlers

logging_format = logging.Formatter("%(asctime)s %(levelname)s %(filename)s %(message)s")
logging_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.log")
log_file = logging.handlers.TimedRotatingFileHandler(
    logging_path, encoding="utf8", interval=1, when="D"
)
log_file.setFormatter(logging_format)
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging_format)
handler.setLevel(logging.ERROR)

logger = logging.getLogger("server")
logger.addHandler(handler)
logger.addHandler(log_file)
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    logger.critical("Критическая ошибка")
    logger.error("Ошибка")
    logger.debug("Отладочная информация")
    logger.info("Информационное сообщение")

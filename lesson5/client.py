import sys
import socket
from functions.func_client import message
from log.client_log_config import logger

DEFAULT_PACKET_SIZE = 1024


class Client:
    __slots__ = ["addr", "port", "socket"]

    def __init__(self, addr="127.0.0.1", port=7777) -> None:
        self.port = port
        self.addr = addr

    def presence(self):
        # print("send socket message")
        logger.debug("send socket message")
        if self.socket.send(message("presence", "I'm here")):
            self.get_message()

    def close(self):
        # print("closing connection")
        logger.debug("closing connection")
        if self.socket.send(message("quit", "quit")):
            self.get_message()

    def get_message(self):
        data = self.socket.recv(DEFAULT_PACKET_SIZE)
        msg = data.decode("utf-8")
        # print(f"[size:{sys.getsizeof(data)}bytes] {msg}")
        logger.debug(f"[size:{sys.getsizeof(data)}bytes] {msg}")

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.addr, self.port))


if __name__ == "__main__":
    # -p 7777 -a 127.0.0.1
    port = 7777
    addr = "127.0.0.1"
    if "-p" in sys.argv:
        port = int(sys.argv[sys.argv.index("-p") + 1])
    if "-a" in sys.argv:
        addr = sys.argv[sys.argv.index("-a") + 1]

    s = Client(addr, port)
    s.connect()
    s.presence()
    s.close()

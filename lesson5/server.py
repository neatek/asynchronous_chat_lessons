import sys
import socket
from functions.func_server import message, read_package
from log.server_log_config import logger

# import select


DEFAULT_PACKET_SIZE = 1024
MAX_CONNECTIONS = 1


class Server:
    __slots__ = ["addr", "port", "socket", "idx"]

    def __init__(self, addr="0.0.0.0", port=7777) -> None:
        self.idx = 0
        self.port = port
        self.addr = addr

    def recv(self, socket):
        data = socket.recv(DEFAULT_PACKET_SIZE)
        data = read_package(data)

        # print(f"[{self.idx}] Received: {data}")
        logger.debug(f"[{self.idx}] Received: {data}")

        self.idx += 1

        msg = message(200, "OK")
        socket.send(msg)
        # print(f"Sended: {msg}")
        logger.debug(f"Sended: {msg}")

        if data["action"] == "quit":
            socket.close()

    def listen(self):
        # print(f"Server listening on {self.addr}:{self.port}")
        logger.debug(f"Server listening on {self.addr}:{self.port}")
        while True:
            socket, client = self.socket.accept()
            while True:
                try:
                    self.recv(socket)
                except:
                    break

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.addr, self.port))
        self.socket.listen(MAX_CONNECTIONS)


if __name__ == "__main__":
    # -p 7777 -a 127.0.0.1
    port = 7777
    addr = "0.0.0.0"
    if "-p" in sys.argv:
        port = int(sys.argv[sys.argv.index("-p") + 1])
    if "-a" in sys.argv:
        addr = sys.argv[sys.argv.index("-a") + 1]

    s = Server(addr, port)
    s.start()
    s.listen()
    print("Server stopped")

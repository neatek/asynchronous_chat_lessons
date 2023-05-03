import sys
import socket
import threading
from functions.decorators import log
from functions.func_server import message, read_package
from functions.func_client import message as client_message
from log.server_log_config import logger

DEFAULT_PACKET_SIZE = 1024
MAX_CONNECTIONS = 10


class Server:
    __slots__ = ["addr", "port", "socket", "idx", "clients", "messages"]

    def __init__(self, addr="0.0.0.0", port=7777) -> None:
        self.idx = 0
        self.port = port
        self.addr = addr
        self.clients = []
        self.messages = []

    @log
    def recv(self, socket):
        try:
            data = socket.recv(DEFAULT_PACKET_SIZE)
        except BaseException as e:
            if socket in self.clients:
                self.clients.remove(socket)
            print(f"Client {socket.getpeername()} has disconnected.")
            socket.close()
            return None

        data = read_package(data)
        if data is None:
            if socket in self.clients:
                self.clients.remove(socket)
            print(f"Client {socket.getpeername()} has disconnected.")
            socket.close()
            return None

        if isinstance(data, dict):
            self.idx += 1
            logger.debug(f"[{self.idx}] Received: {data}")
            for client in self.clients:
                msg = client_message("message", data["message"])
                client.send(msg)
                print(f"Sended: {msg}")
                logger.debug(f"Sended: {msg}")
            if data["action"] == "quit":
                socket.close()
            return data

    def thread_receive_func(self, socket, username):
        print(f"Created new thread ({username})")
        print(self.clients)
        while True:
            if self.recv(socket) is None:
                print(f"Client thread closed.")
                break

    @log
    def listen(self):
        logger.debug(f"Server listening on {self.addr}:{self.port}")
        while True:
            try:
                socket, client = self.socket.accept()
            except OSError:
                pass
            else:
                logger.debug(f"Client {socket.getpeername()} connected.")
                print(f"Client {socket.getpeername()} connected.")
                self.clients.append(socket)

                thread_receive = threading.Thread(
                    target=self.thread_receive_func, args=(socket, socket.getpeername())
                )
                thread_receive.daemon = True
                thread_receive.start()

    @log
    def start(self):
        self.clients = []
        self.messages = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.addr, self.port))
        self.socket.settimeout(0.5)
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

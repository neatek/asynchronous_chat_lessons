import sys
import socket
import select
from functions.decorators import log
from functions.func_server import message, read_package
from log.server_log_config import logger

# import select


DEFAULT_PACKET_SIZE = 1024
MAX_CONNECTIONS = 1


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

        return data

    @log
    def listen(self):
        # print(f"Server listening on {self.addr}:{self.port}")
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

            received_data = []
            send_data = []
            errors = []
            try:
                if self.clients:
                    received_data, send_data, errors = select.select(
                        self.clients, self.clients, [], 0
                    )
            except OSError:
                pass

            if received_data:
                for client in received_data:
                    try:
                        data = self.recv(client)
                        print(f"Received: {data}")
                    except:
                        logger.debug(f"Client {client.getpeername()} has disconnected.")
                        print(f"Client {client.getpeername()} has disconnected.")
                        self.clients.remove(client)

            if send_data:
                del send_data[0]
                for waiting_client in send_data:
                    try:
                        msg = message(200, message)
                        socket.send(msg)
                    except:
                        logger.debug(
                            f"Client {waiting_client.getpeername()} has disconnected."
                        )
                        self.clients.remove(waiting_client)
            # while True:
            #     try:
            #         self.recv(socket)
            #     except:
            #         break

    @log
    def start(self):
        self.clients = []
        self.messages = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

import sys
import socket
import time
import threading
from functions.decorators import log
from functions.func_client import message
from log.client_log_config import logger
from metaclasses import ClientMaker

DEFAULT_PACKET_SIZE = 1024


class Client(metaclass=ClientMaker):
    __slots__ = ["addr", "port", "socket", "thread_sending", "thread_receive"]

    def __init__(self, addr="127.0.0.1", port=7777) -> None:
        self.port = port
        self.addr = addr
        self.thread_sending = None

    @log
    def presence(self):
        logger.debug("send socket message")
        self.socket.send(message("presence", "I'm here"))

    @log
    def close(self):
        # logger.debug("closing connection")
        # self.socket.send(message("quit", "quit"))
        exit()

    @log
    def reconnect(self):
        self.connect()

    @log
    def thread_sending_func(self, socket, username):
        while True:
            msg = input(f"\r\nInput text:")
            if msg:
                try:
                    self.socket.send(message("message", msg))
                except BaseException as e:
                    print(str(e))
                    # break
                    self.reconnect()

    @log
    def thread_receive_func(self, socket, username):
        while True:
            data = None
            try:
                # print("Reading socket")
                data = self.socket.recv(DEFAULT_PACKET_SIZE)
                msg = data.decode("utf-8")
                logger.debug(f"[size:{sys.getsizeof(data)}bytes] {msg}")
                print(f"[Received:{sys.getsizeof(data)}bytes] {msg}")
            except BaseException as e:
                print(str(e))
                break

    @log
    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.setdefaulttimeout(0.5)
        self.socket.setblocking(1)
        # self.socket.settimeout(0.5)
        self.socket.connect((self.addr, self.port))

        print("Connection is still alive, start typing to send message")

        self.presence()

        # Send messages in thread
        self.thread_sending = threading.Thread(
            target=self.thread_sending_func, args=(self.socket, self.port)
        )
        self.thread_sending.daemon = True
        self.thread_sending.start()

        # Receive messages in thread
        self.thread_receive = threading.Thread(
            target=self.thread_receive_func, args=(self.socket, self.port)
        )
        self.thread_receive.daemon = True
        self.thread_receive.start()

    @log
    def is_alive(self):
        if self.thread_sending.is_alive() and self.thread_receive.is_alive():
            return True
        return False


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

    while True:
        time.sleep(1)
        if s.is_alive():
            continue
        break

    s.close()

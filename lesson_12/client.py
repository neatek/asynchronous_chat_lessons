import sys
import socket
import time
import threading
from functions.decorators import log
from functions.func_client import message, MessageFormat
from functions.func_server import read_package
from log.client_log_config import logger
from metaclasses import ClientMaker
from client_database import ClientDatabase

DEFAULT_PACKET_SIZE = 2048
database_lock = threading.Lock()


def print_help():
    print("Доступные команды:")
    print("help - Доступные команды")
    print("msg - Отправить сообщение")
    print("history - История")
    print("contacts - Список контактов")
    print("add - Добавить в контакты")
    print("rm - Удалить из контактов")
    print("exit - Выйти")


class ClientReader(threading.Thread, metaclass=ClientMaker):
    def __init__(self, account_name, sock, database):
        self.account_name = account_name
        self.sock = sock
        self.database = database
        super().__init__()

    def run(self):
        while True:
            data = None
            try:
                data = self.sock.recv(DEFAULT_PACKET_SIZE)
                package = read_package(data)
                print(f"\r\n {package['sender']}: {package['message']}\r\n")
                with database_lock:
                    self.database.save_message(
                        self.account_name, package["receiver"], package["message"]
                    )
            except BaseException as e:
                print(str(e))
                break


def database_load(sock, database, username):
    pass


class ClientSender(threading.Thread):
    def __init__(self, account_name, sock, database):
        self.account_name = account_name
        self.sock = sock
        self.database = database
        super().__init__()

    @log
    def presence(self):
        msg = MessageFormat(
            action="presence",
            message="",
            receiver="",
            sender=self.account_name,
        )
        self.sock.send(message(msg))

    def command_exit(self):
        msg = MessageFormat(
            action="quit",
            message="",
            receiver="",
            sender=self.account_name,
        )
        self.sock.send(message(msg))

    def command_message(self):
        receiver = input(f"\r\nВведите получателя:")
        msg = input(f"\r\nВведите текст:")
        if msg:
            try:
                msg = MessageFormat(
                    action="message",
                    message=msg,
                    receiver=receiver,
                    sender=self.account_name,
                )
                self.sock.send(message(msg))

            except BaseException as e:
                print(str(e))

    def command_contacts(self):
        msg = MessageFormat(
            action="get_contacts",
            message="",
            receiver="",
            sender=self.account_name,
        )
        self.sock.send(message(msg))
        with database_lock:
            contacts_list = self.database.get_contacts()
        for contact in contacts_list:
            print(contact)

    def command_add(self):
        user = input("Введите пользователя для добавления: ")
        msg = MessageFormat(
            action="add_contact",
            message=user,
            receiver=user,
            sender=self.account_name,
        )
        self.sock.send(message(msg))
        with database_lock:
            self.database.add_contact(user)

    def command_rm(self):
        user = input("Введите пользователя для удаления: ")
        msg = MessageFormat(
            action="del_contact",
            message=user,
            receiver=user,
            sender=self.account_name,
        )
        self.sock.send(message(msg))
        with database_lock:
            self.database.del_contact(user)

    def command_history(self):
        with database_lock:
            history_list = self.database.get_history(to_who=self.account_name)
            for message in history_list:
                print(
                    f"\nСообщение от пользователя: {message[0]} от {message[3]}:\n{message[2]}"
                )

    @log
    def run(self):
        while True:
            cmd = input("")
            if cmd == "msg":
                self.command_message()
            elif cmd == "help":
                print_help()
            elif cmd == "contacts":
                self.command_contacts()
            elif cmd == "add":
                self.command_add()
            elif cmd == "rm":
                self.command_rm()
            elif cmd == "history":
                self.command_history()
            elif cmd == "exit":
                self.command_exit()
                exit()


if __name__ == "__main__":
    port = 7777
    addr = "127.0.0.1"
    if "-p" in sys.argv:
        port = int(sys.argv[sys.argv.index("-p") + 1])
    if "-a" in sys.argv:
        addr = sys.argv[sys.argv.index("-a") + 1]

    client_name = input("Type name of client: ")
    print_help()
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect(("127.0.0.1", 7777))

    msg = MessageFormat(
        action="presence",
        message="Hello world",
        receiver="",
        sender=client_name,
    )
    socket.send(message(msg))

    database = ClientDatabase(client_name)
    database_load(socket, database, client_name)

    module_receiver = ClientReader(client_name, socket, database)
    module_receiver.daemon = True
    module_receiver.start()

    module_sender = ClientSender(client_name, socket, database)
    module_sender.daemon = True
    module_sender.start()

    while True:
        time.sleep(1)
        if module_receiver.is_alive() and module_sender.is_alive():
            continue
        break

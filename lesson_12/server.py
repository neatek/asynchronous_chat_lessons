from collections.abc import Callable, Iterable, Mapping
import sys
import socket
import os
import argparse
import threading
import select
import configparser
from functions.decorators import log
from functions.func_server import message, read_package
from functions.func_client import message as client_message, MessageFormat
from log.server_log_config import logger
from descrptrs import Port
from metaclasses import ServerMaker
from server_database import ServerStorage
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer
from server_gui import (
    MainWindow,
    gui_create_model,
    HistoryWindow,
    create_stat_model,
    ConfigWindow,
)

DEFAULT_PACKET_SIZE = 2048
MAX_CONNECTIONS = 10
new_connection = False
conflag_lock = threading.Lock()
database_lock = threading.Lock()
new_connection = False


@log
def arg_parser(default_port, default_address):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", default=default_port, type=int, nargs="?")
    parser.add_argument("-a", default=default_address, nargs="?")
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    return listen_address, listen_port


class Server(threading.Thread, metaclass=ServerMaker):
    port = Port()

    def __init__(
        self, addr="0.0.0.0", port=7777, database: ServerStorage = None
    ) -> None:
        self.addr = addr
        self.port = port
        self.transport = None
        self.clients = []
        self.messages = []
        self.database = database
        self.names = {}
        super().__init__()

    def add_name(self, client, name):
        print(f"Added name {name} with socket {client}")
        self.names[name] = client

    def get_name(self, client):
        for key, name in self.names.items():
            if name == client:
                return key

    def get_socket_by_name(self, name):
        for named, client in self.names.items():
            if named == name:
                return client

    def remove_name(self, client):
        for name in self.names:
            if name == client:
                del self.names[name]

    def send_message_to(self, data: MessageFormat):
        print(data)
        client = self.get_socket_by_name(data.receiver)
        if client is not None:
            client.send(client_message(data))
            print(f"Sended: {data.message} to {data.receiver} from {data.sender}")
            logger.debug(
                f"Sended: {data.message} to {data.receiver} from {data.sender}"
            )

    def on_disconnect(self, client):
        self.database.user_logout(self.get_name(client))
        self.remove_name(client)
        if client in self.clients:
            self.clients.remove(client)
        print(f"Client {client.getpeername()} has disconnected.")
        client.close()
        global new_connection
        with conflag_lock:
            new_connection = True

    def on_connect(self, client):
        logger.debug(f"Client {client.getpeername()} connected.")
        print(f"Client {client.getpeername()} connected.")
        self.clients.append(client)

    @log
    def read_package(self, client):
        try:
            data = client.recv(DEFAULT_PACKET_SIZE)
        except BaseException as e:
            self.on_disconnect(client)
            return None

        data = read_package(data)
        if data is None:
            self.on_disconnect(client)
            return None

        if isinstance(data, dict):
            global new_connection
            # Message
            if data["action"] == "message":
                new_data = MessageFormat(
                    action="message",
                    message=data["message"],
                    receiver=data["receiver"],
                    sender=data["sender"],
                )
                self.database.process_message(data["sender"], data["receiver"])
                self.send_message_to(new_data)
            # Presence
            elif data["action"] == "presence":
                account_name = data["sender"]
                self.add_name(client, account_name)
                client_ip, client_port = client.getpeername()
                self.database.user_login(account_name, client_ip, client_port)
                with conflag_lock:
                    new_connection = True
            # Get contacts
            elif data["action"] == "get_contacts":
                # contacts_list = self.database.get_contacts()
                print("get_contacts")
            # Add contacts
            elif data["action"] == "add_contact":
                print("add_contact")
            # Remove contacts
            elif data["action"] == "del_contact":
                print("del_contact")
            # Quit
            elif data["action"] == "quit":
                self.on_disconnect(client)
                with conflag_lock:
                    new_connection = True
            return data

    def run(self):
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)

        self.transport = transport
        self.transport.listen()

        logger.debug(f"Server listening on {self.addr}:{self.port}")

        while True:
            try:
                client, client_address = transport.accept()
            except OSError:
                pass
            else:
                self.on_connect(client)

            recv_waiting = []
            send_waiting = []
            err_lst = []
            try:
                if self.clients:
                    recv_waiting, send_waiting, err_lst = select.select(
                        self.clients, self.clients, [], 0
                    )
            except OSError as err:
                logger.error(f"{err}")

            if recv_waiting:
                for client_socket in recv_waiting:
                    try:
                        self.read_package(client_socket)
                    except OSError:
                        self.on_disconnect(client_socket)


def main():
    # Загрузка файла конфигурации сервера
    config = configparser.ConfigParser()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    config.read(f"{dir_path}/{'server.ini'}")

    # Загрузка параметров командной строки, если нет параметров, то задаём
    # значения по умоланию.
    listen_address, listen_port = arg_parser(
        config["SETTINGS"]["Default_port"], config["SETTINGS"]["Listen_Address"]
    )

    # Инициализация базы данных
    database = ServerStorage(
        os.path.join(
            config["SETTINGS"]["Database_path"], config["SETTINGS"]["Database_file"]
        )
    )

    # Создание экземпляра класса - сервера и его запуск:
    server = Server(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    # Создаём графическое окуружение для сервера:
    server_app = QApplication(sys.argv)
    main_window = MainWindow()

    # Инициализируем параметры в окна
    main_window.statusBar().showMessage("Server Working")
    main_window.active_clients_table.setModel(gui_create_model(database))
    main_window.active_clients_table.resizeColumnsToContents()
    main_window.active_clients_table.resizeRowsToContents()

    # Функция обновляющяя список подключённых, проверяет флаг подключения, и
    # если надо обновляет список
    def list_update():
        global new_connection
        if new_connection:
            main_window.active_clients_table.setModel(gui_create_model(database))
            main_window.active_clients_table.resizeColumnsToContents()
            main_window.active_clients_table.resizeRowsToContents()
            with conflag_lock:
                new_connection = False

    # Функция создающяя окно со статистикой клиентов
    def show_statistics():
        global stat_window
        stat_window = HistoryWindow()
        stat_window.history_table.setModel(create_stat_model(database))
        stat_window.history_table.resizeColumnsToContents()
        stat_window.history_table.resizeRowsToContents()
        stat_window.show()

    # Функция создающяя окно с настройками сервера.
    def server_config():
        global config_window
        # Создаём окно и заносим в него текущие параметры
        config_window = ConfigWindow()
        config_window.db_path.insert(config["SETTINGS"]["Database_path"])
        config_window.db_file.insert(config["SETTINGS"]["Database_file"])
        config_window.port.insert(config["SETTINGS"]["Default_port"])
        config_window.ip.insert(config["SETTINGS"]["Listen_Address"])
        config_window.save_btn.clicked.connect(save_server_config)

    # Функция сохранения настроек
    def save_server_config():
        global config_window
        message = QMessageBox()
        config["SETTINGS"]["Database_path"] = config_window.db_path.text()
        config["SETTINGS"]["Database_file"] = config_window.db_file.text()
        try:
            port = int(config_window.port.text())
        except ValueError:
            message.warning(config_window, "Ошибка", "Порт должен быть числом")
        else:
            config["SETTINGS"]["Listen_Address"] = config_window.ip.text()
            if 1023 < port < 65536:
                config["SETTINGS"]["Default_port"] = str(port)
                with open("server.ini", "w") as conf:
                    config.write(conf)
                    message.information(
                        config_window, "OK", "Настройки успешно сохранены!"
                    )
            else:
                message.warning(
                    config_window, "Ошибка", "Порт должен быть от 1024 до 65536"
                )

    # Таймер, обновляющий список клиентов 1 раз в секунду
    timer = QTimer()
    timer.timeout.connect(list_update)
    timer.start(1000)

    # Связываем кнопки с процедурами
    main_window.refresh_button.triggered.connect(list_update)
    main_window.show_history_button.triggered.connect(show_statistics)
    main_window.config_btn.triggered.connect(server_config)

    # Запускаем GUI
    server_app.exec_()


if __name__ == "__main__":
    # -p 7777 -a 127.0.0.1
    main()

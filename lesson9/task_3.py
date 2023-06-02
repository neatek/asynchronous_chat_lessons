from tabulate import tabulate
from task_2 import host_range_ping


def host_range_ping_tab():
    results = host_range_ping()
    tabulate_tables = {"IP Address": [], "Reach": []}
    for result in results:
        tabulate_tables["IP Address"].append(result[0])
        tabulate_tables["Reach"].append("✅" if result[1] == "Reachable" else "❌")
    print(tabulate(tabulate_tables, headers="keys"))


if __name__ == "__main__":
    host_range_ping_tab()

"""
Введите первоначальный адрес: 192.168.1.1
Сколько адресов проверить?: 10
IP Address    Reach
------------  -------
192.168.1.1   ❌
192.168.1.2   ❌
192.168.1.3   ✅
192.168.1.4   ✅
192.168.1.5   ✅
192.168.1.6   ✅
192.168.1.7   ✅
192.168.1.8   ✅
192.168.1.9   ✅
192.168.1.10  ❌
"""

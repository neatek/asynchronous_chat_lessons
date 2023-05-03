from ipaddress import ip_address
from task_1 import host_ping


def host_range_ping():
    while True:
        start_ip = input("Введите первоначальный адрес: ")
        try:
            las_oct = int(start_ip.split(".")[3])
            break
        except Exception as e:
            print(e)

    while True:
        end_ip = input("Сколько адресов проверить?: ")
        if not end_ip.isnumeric():
            print("Необходимо ввести число: ")
        else:
            if (las_oct + int(end_ip)) > 254:
                print(
                    f"Можем менять только последний октет, т.е. "
                    f"максимальное число хостов для проверки: {254-las_oct}"
                )
            else:
                break

    host_list = []
    [host_list.append(str(ip_address(start_ip) + x)) for x in range(int(end_ip))]
    return host_ping(host_list)


if __name__ == "__main__":
    host_range_ping()

""" 
Введите первоначальный адрес: 192.168.1.1
Сколько адресов проверить?: 100
192.168.1.1[Unreachable]
192.168.1.2[Reachable]
192.168.1.3[Reachable]
192.168.1.4[Reachable]
192.168.1.5[Reachable]
192.168.1.6[Reachable]
192.168.1.7[Unreachable]
192.168.1.8[Unreachable]
192.168.1.9[Reachable]
192.168.1.10[Reachable]
192.168.1.11[Reachable]
192.168.1.12[Reachable]
192.168.1.13[Reachable]
192.168.1.14[Reachable]
192.168.1.15[Reachable]
192.168.1.16[Unreachable]
192.168.1.17[Unreachable]
192.168.1.18[Reachable]
192.168.1.19[Reachable]
192.168.1.20[Reachable]
192.168.1.21[Reachable]
192.168.1.22[Reachable]
192.168.1.23[Reachable]
192.168.1.24[Reachable]
192.168.1.25[Reachable]
192.168.1.26[Unreachable]
192.168.1.27[Unreachable]
192.168.1.28[Reachable]
192.168.1.29[Reachable]
192.168.1.30[Reachable]
192.168.1.31[Reachable]
192.168.1.32[Reachable]
192.168.1.33[Reachable]
192.168.1.34[Reachable]
192.168.1.35[Unreachable]
192.168.1.36[Unreachable]
192.168.1.37[Reachable]
192.168.1.38[Reachable]
192.168.1.39[Reachable]
192.168.1.40[Reachable]
192.168.1.41[Reachable]
192.168.1.42[Reachable]
192.168.1.43[Unreachable]
192.168.1.44[Unreachable]
192.168.1.45[Reachable]
192.168.1.46[Reachable]
192.168.1.47[Reachable]
192.168.1.48[Reachable]
192.168.1.49[Reachable]
192.168.1.50[Unreachable]
192.168.1.51[Unreachable]
192.168.1.52[Reachable]
192.168.1.53[Reachable]
192.168.1.54[Reachable]
192.168.1.55[Reachable]
192.168.1.56[Reachable]
192.168.1.57[Reachable]
192.168.1.58[Reachable]
192.168.1.59[Reachable]
192.168.1.60[Reachable]
192.168.1.61[Reachable]
192.168.1.62[Unreachable]
192.168.1.63[Unreachable]
192.168.1.64[Reachable]
192.168.1.65[Reachable]
192.168.1.66[Reachable]
192.168.1.67[Unreachable]
192.168.1.68[Unreachable]
192.168.1.69[Reachable]
192.168.1.70[Reachable]
192.168.1.71[Reachable]
192.168.1.72[Reachable]
192.168.1.73[Reachable]
192.168.1.74[Reachable]
192.168.1.75[Reachable]
192.168.1.76[Reachable]
192.168.1.77[Unreachable]
192.168.1.78[Unreachable]
192.168.1.79[Reachable]
192.168.1.80[Reachable]
192.168.1.81[Reachable]
192.168.1.82[Reachable]
192.168.1.83[Reachable]
192.168.1.84[Reachable]
192.168.1.85[Reachable]
192.168.1.86[Reachable]
192.168.1.87[Reachable]
192.168.1.88[Unreachable]
192.168.1.89[Unreachable]
192.168.1.90[Reachable]
192.168.1.91[Reachable]
192.168.1.92[Reachable]
192.168.1.93[Unreachable]
192.168.1.94[Unreachable]
192.168.1.95[Reachable]
192.168.1.96[Reachable]
192.168.1.97[Reachable]
192.168.1.98[Reachable]
192.168.1.99[Reachable]
192.168.1.100[Reachable]
"""

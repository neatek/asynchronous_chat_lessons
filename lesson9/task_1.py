from ipaddress import ip_address
from subprocess import Popen, PIPE


def host_ping(
    list_ip_addresses: list,
    timeout: int = 10,
    requests: int = 1,
    is_print: bool = False,
):
    results = []
    for address in list_ip_addresses:
        res_string = f"{address}"

        try:
            address = ip_address(address)
        except ValueError:
            pass

        proc = Popen(
            f"ping {address} -w {timeout} -n {requests}", shell=False, stdout=PIPE
        )
        proc.wait()

        # key = 0 if proc.returncode == 0 else 1
        key_text = "Reachable" if proc.returncode == 0 else "Unreachable"
        # results[key] = results[0] + f"{str(address)}[{key_text}]\r\n"
        results.append([str(address), key_text])

    if is_print is True:
        print(results)

    return results


if __name__ == "__main__":
    ip_addresses = [
        "facebook.com",
        "instagram.com",
        "8.8.8.8",
        "8.8.4.4",
        "192.168.1.1",
        "192.168.0.1",
        "yandex.ru",
    ]
    host_ping(ip_addresses, is_print=True)

""" 
facebook.com[Reachable]
instagram.com[Unreachable]
8.8.8.8[Reachable]
8.8.4.4[Reachable]
192.168.1.1[Unreachable]
192.168.0.1[Reachable]
yandex.ru[Reachable]
"""

# Task1

task1 = ["разработка", "сокет", "декоратор"]

for task in task1:
    print(task, type(task))

task1 = [
    "\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430",
    "\u0441\u043e\u043a\u0435\u0442",
    "\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440",
]

for task in task1:
    print(task, type(task))

# Task 2

task2 = [b"class", b"function", b"method"]

for task in task2:
    print(task, type(task))

# Task 3
# SyntaxError: bytes can only contain ASCII literal characters -> b"класс", b"функция"
task3 = ["attribute", "type", "класс", "функция"]

for task in task3:
    try:
        print(bytes(task, "ascii"))
    except:
        print(f"Error -> {task}")

# Task 4
task4 = ["разработка", "администрирование", "protocol", "standard"]

for index, task in enumerate(task4):
    task4[index] = task.encode()

print(task4)

for index, task in enumerate(task4):
    task4[index] = task.decode()

print(task4)

# Task 5
task5 = ["yandex.ru", "youtube.com"]

from chardet import detect
import subprocess

# import os


def ping(host):
    process = subprocess.Popen(
        ["ping", "-n", "1", host], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    streamdata = process.communicate()[0]
    return streamdata


for task in task5:
    # response = os.system("ping -n 1 " + task)
    response = ping(task)
    response = response.decode(detect(response)["encoding"]).encode("utf-8")
    print(response.decode())


# Task 6
task6 = ["сетевое программирование", "сокет", "декоратор"]

with open("lesson_1.txt", "w") as file:
    file.writelines(task6)

detected_encoding = "utf-8"
with open("lesson_1.txt", "rb") as file:
    text = file.read()
    detected_encoding = detect(text)["encoding"]

print(detected_encoding)

with open("lesson_1.txt", "r", encoding=detected_encoding) as file:
    text = file.read()
    print(text)

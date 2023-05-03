import subprocess

processing = []

while True:
    user_input = input("Enter NUMBER of client apps (q - close): ")

    if user_input == "q":
        while processing:
            subproc = processing.pop()
            subproc.kill()
        exit()

    else:
        processing.append(
            subprocess.Popen(
                "python server.py", creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        )
        for i in range(int(user_input)):
            processing.append(
                subprocess.Popen(
                    "python client.py", creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            )

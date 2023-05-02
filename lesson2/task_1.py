# Task 1
import re
import csv
import os.path


def get_data(files: list):
    main_data = []
    main_data.append(
        ["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]
    )
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    for file in files:
        with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), file), "r"
        ) as file:
            lines = file.readlines()
            lines = "\r\n".join(lines)
            row = []
            for index, title in enumerate(main_data[0]):
                result = re.findall(rf"{title}:(.*)$", lines, re.MULTILINE)
                if result is not None and len(result) > 0:
                    result = result[0].strip()
                    if index == 0:
                        os_prod_list.append(result)
                    elif index == 1:
                        os_name_list.append(result)
                    elif index == 2:
                        os_code_list.append(result)
                    elif index == 3:
                        os_type_list.append(result)
                    row.append(result)
            main_data.append(row)
    return main_data


def write_to_csv(file_path):
    files = [
        "info_1.txt",
        "info_2.txt",
        "info_3.txt",
    ]
    result = get_data(files)
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path),
        "w",
        encoding="utf-8",
    ) as file:
        csv_handler = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=";")
        for row in result:
            csv_handler.writerow(row)


write_to_csv("output.txt")

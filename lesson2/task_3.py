import yaml
import os.path


data = {"list": ["list1", "list2"], "numbers": [1, 2, 3, 4, 5], "three": {"€": 123}}
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "file.yaml")

with open(file_path, "w+", encoding="utf-8") as file:
    yaml.dump(data, file, default_flow_style=True, allow_unicode=True)

with open(file_path, encoding="utf-8") as file:
    print(file.read())

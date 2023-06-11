import json
import os.path
from datetime import datetime


def write_order_to_json(item, quantity, price: float, buyer, date: datetime):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "orders.json")
    date = str(date)
    data = '{"orders":[]}'

    with open(file_path, "r") as file:
        data = file.readlines()
        if len(data) > 0:
            data = "".join(data)
            data = json.loads(data)

    with open(file_path, "w") as file:
        data["orders"].append(
            {
                "item": item,
                "quantity": quantity,
                "price": price,
                "buyer": buyer,
                "data": date,
            }
        )
        file.truncate(0)
        file.write(json.dumps(data, indent=4))


write_order_to_json("My Item 1", 10, 100.0, "Artyom Vasiliev", datetime.now())
write_order_to_json("My Item 2", 5, 50.0, "Artyom Vasiliev", datetime.now())

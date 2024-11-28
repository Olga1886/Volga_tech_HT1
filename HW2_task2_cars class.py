import json
from typing import List, Union

class CarsDataset:
    def __init__(self, json_file_path: str):
        with open(json_file_path, "r") as f:
            self.data = json.load(f)["cars"]  # Загружаем данные из json файла

    def get_items(self, properties: dict) -> Union[List[str], str]:
        output_list = []
        for car in self.data:
            if all(car.get(key) in value for key, value in properties.items()):
                output_list.append(car["path"])
        return output_list

# Test
json_file_path = r"C:\Users\Lenovo\PycharmProjects\Volga_tech_HT1\HW2\t2_data\cars\cars.json"
cars_database = CarsDataset(json_file_path)
properties = {"type": "hatchback", "mark": "toyota"}
print(cars_database.get_items(properties))

properties = {"type": ["hatchback", "sedan"], "mark": ["vw", "bmw"]}
print(cars_database.get_items(properties))

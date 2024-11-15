import json
import os
from typing import Union, List


def get_mark(f: str) -> str:
    return f[0].split('_')[-1]

def create_dataset_json(root_folder: str, json_file: str):
    dataset_json = []
    for r, d, f in os.walk(root_folder):
        for file in f:
            if file.endswith(".jpeg"):
                instance = dict()
                image_path = os.path.join(r, file)
                instance["path"] = os.path.relpath(image_path, os.path.commonpath([image_path, json_file]))
                instance["type"] = os.path.split(r)[-1]
                instance["mark"] = get_mark(file.split('.')[:-1])
                dataset_json.append(instance)
    json_data = {"cars": dataset_json}
    with open(json_file, 'w') as file:
        json.dump(json_data, file, indent=4)


# r=root, d=directories, f = files
thisdir = r"C:\Users\Lenovo\PycharmProjects\Volga_tech_HT1\HW2\t2_data\cars"
json_file = os.path.join(thisdir, 'cars.json')
create_dataset_json(thisdir, json_file)






















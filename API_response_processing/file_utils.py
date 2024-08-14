# ./file_utils.py
import os
import json
import logging

def save_json_to_file(data, path, description):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)
    logging.debug(f"{description} saved to '{path}'")

def load_json_from_file(path):
    with open(path, 'r') as file:
        return json.load(file)

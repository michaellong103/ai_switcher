# ./dynamic_timespans/load_data.py

import json
from testing.find_file import find_file

def load_data(filename):
    """
    Load the specified JSON file using the find_file function.
    """
    file_path = find_file(filename)
    with open(file_path, "r") as file:
        return json.load(file)

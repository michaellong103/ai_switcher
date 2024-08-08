# ./API_response_processing/file_utils.py

import os
import json
import logging


def save_json_to_file(data, path, description):
    """
    Saves data to a JSON file.

    Args:
        data (dict or list): Data to save.
        path (str): File path to save the JSON.
        description (str): Description of the data being saved.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)
    logging.debug(f"{description} saved to '{path}'")


def load_json_from_file(path):
    """
    Loads data from a JSON file.

    Args:
        path (str): File path to load the JSON.

    Returns:
        dict or list: Loaded JSON data.
    """
    with open(path, 'r') as file:
        return json.load(file)

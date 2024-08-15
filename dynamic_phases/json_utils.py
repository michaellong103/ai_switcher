# ./dynamic_phases/json_utils.py

import json
import os

def load_json_data(filepath):
    """Loads JSON data from a file."""
    if not os.path.exists(filepath):
        print(f"Error: {filepath} does not exist.")
        return None

    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON data from {filepath}: {e}")
        return None

def save_json_data(filepath, data):
    """Saves data as JSON to a file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data successfully saved to {filepath}")
    except Exception as e:
        print(f"Error saving JSON data to {filepath}: {e}")

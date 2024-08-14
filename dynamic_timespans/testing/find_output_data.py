# ./testing/find_output_data.py

import os
import json

def find_output_data(filename='output_data.json'):
    """
    Attempt to find the specified file in multiple possible locations.
    Returns the data if the file is found, otherwise raises a FileNotFoundError.
    """
    # List of potential paths to check for the file
    possible_paths = [
        (filename, "filename,  # Current directory"),
        (os.path.join(os.path.dirname(__file__), filename), "os.path.join(os.path.dirname(__file__), filename),  # Same directory as the script"),
        (os.path.join(os.path.dirname(__file__), '..', filename), "os.path.join(os.path.dirname(__file__), '..', filename),  # One level up from the current directory"),
        (os.path.join(os.path.dirname(__file__), '..', 'dynamic_timespans', filename), "os.path.join(os.path.dirname(__file__), '..', 'dynamic_timespans', filename),  # dynamic_timespans directory"),
        (os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', filename)), "os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', filename)),  # Absolute path to two levels up from the current directory"),
        (os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'dynamic_timespans', filename)), "os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'dynamic_timespans', filename)),  # Absolute path to dynamic_timespans"),
    ]

    for path, description in possible_paths:
        if os.path.exists(path):
            print(f"Found file at: {path} using {description}")
            with open(path, "r") as file:
                return json.load(file)
    
    # If the file is not found in any of the paths, raise an error
    raise FileNotFoundError(f"File {filename} not found in any of the expected locations.")

if __name__ == "__main__":
    try:
        data = find_output_data()
        print("File found and loaded successfully!")
        print(json.dumps(data, indent=2))
    except FileNotFoundError as e:
        print(e)

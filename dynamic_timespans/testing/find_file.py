# ./dynamic_timespans/testing/find_file.py

import os

def find_file(filename):
    """
    Try to locate the specified file in various expected locations and return the first found path.
    """
    # List of possible paths to check
    paths_to_check = [
        (filename, "filename,  # Current directory"),
        (os.path.join(os.path.dirname(__file__), filename), "os.path.join(os.path.dirname(__file__), filename),  # Same directory as the script"),
        (os.path.join(os.path.dirname(__file__), '..', filename), "os.path.join(os.path.dirname(__file__), '..', filename),  # One level up from the current directory"),
        (os.path.join(os.path.dirname(__file__), '..', 'dynamic_timespans', filename), "os.path.join(os.path.dirname(__file__), '..', 'dynamic_timespans', filename),  # dynamic_timespans directory"),
        (os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', filename)), "os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', filename)),  # Absolute path to two levels up from the current directory"),
        (os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'dynamic_timespans', filename)), "os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'dynamic_timespans', filename)),  # Absolute path to dynamic_timespans"),
        (os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'JSON', filename)), "os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'JSON', filename)),  # Absolute path to JSON directory"),
        (os.path.join(os.path.dirname(__file__), '..', 'JSON', filename), "os.path.join(os.path.dirname(__file__), '..', 'JSON', filename),  # JSON directory one level up"),
        (os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'JSON', filename)), "os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'JSON', filename)),  # Absolute path to JSON directory from tools"),
    ]

    for path, description in paths_to_check:
        print(f"Checking path: {path} using {description}")
        if os.path.isfile(path):
            print(f"Found file at: {path} using {description}")
            return path  # Return the first found path as a string

    raise FileNotFoundError(f"File {filename} not found in any of the expected locations.")

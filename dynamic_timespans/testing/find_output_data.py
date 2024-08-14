# ./testing/find_output_data.py
import os
import json
import unittest
from unittest.mock import patch, mock_open

def find_output_data(filename='output_data.json'):
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
    
    raise FileNotFoundError(f"File {filename} not found in any of the expected locations.")

class TestFindOutputData(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    @patch('os.path.exists', return_value=True)
    def test_find_output_data(self, mock_exists, mock_open):
        data = find_output_data('output_data.json')
        self.assertEqual(data, {"key": "value"})

if __name__ == "__main__":
    unittest.main()

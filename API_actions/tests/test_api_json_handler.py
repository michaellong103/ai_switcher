# ./tests/test_api_json_handler.py

import unittest
import json
from api_actions.api_json_handler import read_json, write_json

class TestJsonHandler(unittest.TestCase):
    def test_read_json(self):
        with open('test_input.json', 'w') as file:
            json.dump({"key": "value"}, file)

        data = read_json('test_input.json')
        self.assertEqual(data, {"key": "value"})

    def test_write_json(self):
        data = {"key": "value"}
        write_json(data, 'test_output.json')

        with open('test_output.json', 'r') as file:
            result = json.load(file)
        
        self.assertEqual(result, data)

if __name__ == '__main__':
    unittest.main()

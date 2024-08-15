# ./dynamic_timespans/testing/test_file_loading.py

import unittest
from unittest.mock import patch, mock_open
from testing.find_file import find_file
from load_data import load_data

class TestFileLoading(unittest.TestCase):

    def setUp(self):
        # Print the name of the file in purple before each test
        print("\033[95mRunning tests in: ./testing/test_file_loading.py\033[0m")

    @patch('os.path.isfile', return_value=True)
    def test_file_existence(self, mock_isfile):
        # Simulate different file locations and ensure correct path is returned
        file_path = find_file('example.json')
        self.assertTrue(file_path.endswith('example.json'))

    @patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
    @patch('os.path.isfile', return_value=True)
    def test_data_loading(self, mock_isfile, mock_open):
        # Ensure the correct data is loaded from the found file
        data = load_data('example.json')
        self.assertIsInstance(data, dict)
        self.assertEqual(data, {"key": "value"})

if __name__ == '__main__':
    unittest.main()

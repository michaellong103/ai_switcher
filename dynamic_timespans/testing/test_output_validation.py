# ./dynamic_timespans/testing/test_output_validation.py

import unittest
from compare_data import compare_sorted_data

class TestOutputValidation(unittest.TestCase):

    def setUp(self):
        # Print the name of the file in purple before each test
        print("\033[95mRunning tests in: ./testing/test_output_validation.py\033[0m")

    def test_sorted_data(self):
        original_data = [{'daysUntilEnd': 10}, {'daysUntilEnd': 5}, {'daysUntilEnd': 15}]
        sorted_data = [{'daysUntilEnd': 5}, {'daysUntilEnd': 10}, {'daysUntilEnd': 15}]

        # This should pass as the sorted data is correctly ordered
        compare_sorted_data(sorted_data, original_data)

if __name__ == '__main__':
    unittest.main()

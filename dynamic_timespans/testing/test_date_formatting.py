# ./dynamic_timespans/testing/test_date_formatting.py

import unittest
from calculate_data import format_date

class TestDateFormatting(unittest.TestCase):

    def setUp(self):
        # Print the name of the file in purple with ****** on both sides
        print("\033[95m****** Running tests in: ./testing/test_date_formatting.py ******\033[0m")

    def test_date_formatting(self):
        test_data = {
            '2023-12': '31 December 2023',
            '2024-07-16': '16 July 2024'
        }

        for original_date, expected_human_readable_date in test_data.items():
            formatted_date = format_date(original_date)
            self.assertEqual(
                formatted_date, expected_human_readable_date, 
                f"Mismatch: Original Date: {original_date} vs Expected: {expected_human_readable_date}"
            )

if __name__ == '__main__':
    unittest.main()

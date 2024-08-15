# ./testing/test_order_of_entries.py

import unittest
import json
import os
from datetime import datetime

class TestOrderOfEntries(unittest.TestCase):

    def setUp(self):
        # Print the name of the file in purple with ****** on both sides
        print("\033[95m****** Running tests in: ./testing/test_order_of_entries.py ******\033[0m")

        # Load data from ../output_data.json
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output_data.json'))
        with open(file_path, 'r') as file:
            self.data = json.load(file)

    def test_order_of_days_until_end_and_human_readable_date(self):
        for group in self.data:
            # Extract the list of daysUntilEnd values
            days_until_end_values = [
                list(trial.values())[0]['daysUntilEnd'] for trial in group['nctNumbers']
            ]
            
            # Extract the list of humanReadableDate values and convert them to datetime objects
            human_readable_dates = [
                datetime.strptime(list(trial.values())[0]['humanReadableDate'], "%d %B %Y") for trial in group['nctNumbers']
            ]
            
            # Check if the list is sorted in ascending order for daysUntilEnd
            self.assertEqual(days_until_end_values, sorted(days_until_end_values),
                             f"Entries in {group['trialGroup']} are not sorted by 'daysUntilEnd'.")
            
            # Check if the list is sorted in ascending order for humanReadableDate
            self.assertEqual(human_readable_dates, sorted(human_readable_dates),
                             f"Entries in {group['trialGroup']} are not sorted by 'humanReadableDate'.")

if __name__ == '__main__':
    unittest.main()

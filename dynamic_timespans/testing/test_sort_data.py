# ./testing/test_sort_data.py

import unittest
import json
import os
from sort_data import sort_by_days_until_end

class TestSortData(unittest.TestCase):

    def setUp(self):
        # Print the name of the file in purple with ****** on both sides
        print("\033[95m****** Running tests in: ./testing/test_sort_data.py ******\033[0m")

    def load_json_data(self):
        # Load data from ../output_data.json
        print("\033[97mLoading data from '../output_data.json'.\033[0m")
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../output_data.json'))
        with open(file_path, 'r') as file:
            data = json.load(file)
        print("\033[97mData successfully loaded from '../output_data.json'.\033[0m")
        return data

    def test_sort_by_days_until_end(self):
        # Test sorting by 'daysUntilEnd' using real data from JSON file
        print("\033[97mTest sorting by 'daysUntilEnd' using real data from JSON file.\033[0m")
        
        # Load the data from JSON
        data = self.load_json_data()

        # Extract trials from the first group (for example)
        trials = data[0]['nctNumbers']

        # Flatten the list of dictionaries to a single list of trial dictionaries
        flattened_trials = []
        for trial in trials:
            for nct_number, trial_data in trial.items():
                trial_data['nctNumber'] = nct_number
                flattened_trials.append(trial_data)

        # Execute the sort function
        sorted_trials = sort_by_days_until_end(flattened_trials)

        # Check if the trials are sorted correctly by daysUntilEnd
        sorted_days_until_end = [trial.get('daysUntilEnd') for trial in sorted_trials]
        expected_order = sorted(sorted_days_until_end, key=lambda x: x if x is not None else float('inf'))
        self.assertEqual(sorted_days_until_end, expected_order)
        print(f"\033[97mSorted trials by 'daysUntilEnd': {sorted_days_until_end}\033[0m")
        print("\033[97mThe data was sorted correctly by 'daysUntilEnd'.\033[0m")

    def test_sort_empty_list(self):
        # Test sorting an empty list to ensure it returns an empty list
        print("\033[97mTest sorting an empty list to ensure it returns an empty list.\033[0m")
        
        trials = []
        sorted_trials = sort_by_days_until_end(trials)
        self.assertEqual(sorted_trials, [])
        print("\033[97mEmpty list sorting returned an empty list as expected.\033[0m")

    def test_sort_single_element(self):
        # Test sorting a single trial to ensure it remains unchanged
        print("\033[97mTest sorting a single trial to ensure it remains unchanged.\033[0m")
        
        trials = [{"nctNumber": "NCT001", "daysUntilEnd": 10}]
        sorted_trials = sort_by_days_until_end(trials)
        self.assertEqual(sorted_trials, trials)
        print("\033[97mSingle element sorting remained unchanged as expected.\033[0m")

if __name__ == '__main__':
    unittest.main()

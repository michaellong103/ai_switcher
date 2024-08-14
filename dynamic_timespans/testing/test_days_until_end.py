# ./testing/test_days_until_end.py
import unittest
import json
import logging
from dynamic_timespans.testing.find_file import find_file
from dynamic_timespans.main import main as generate_output
from dynamic_timespans.trial_utils import get_all_nct_numbers

logging.basicConfig(level=logging.INFO)

class TestDaysUntilEnd(unittest.TestCase):

    def setUp(self):
        self.original_data = find_file("sort_debug_extracted.json")
        with open(self.original_data, "r") as file:
            self.original_trials = json.load(file)
        generate_output()

    def test_days_until_end(self):
        with open("output_data.json", "r") as file:
            output_data = json.load(file)

        original_trials = self.original_trialstree
        output_trials = output_data

        # Debugging statement to print the structure of original_trials
        logging.info(f"Original trials: {original_trials}")
        logging.info(f"Output trials: {output_trials}")

        original_nct_numbers = get_all_nct_numbers(original_trials)
        output_nct_numbers = get_all_nct_numbers(output_trials)

        self.assertEqual(len(original_trials), len(output_trials))
        self.assertEqual(len(original_nct_numbers), len(output_nct_numbers))

        missing_nct_numbers = original_nct_numbers - output_nct_numbers
        extra_nct_numbers = output_nct_numbers - original_nct_numbers

        self.assertFalse(missing_nct_numbers, f"Missing NCT numbers in output: {missing_nct_numbers}")
        self.assertFalse(extra_nct_numbers, f"Extra NCT numbers in output: {extra_nct_numbers}")

if __name__ == "__main__":
    unittest.main()

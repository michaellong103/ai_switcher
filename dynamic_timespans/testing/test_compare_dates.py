# ./testing/test_compare_dates.py

import sys
import os
import unittest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from calculate_data import format_date

COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"

class TestDateComparison(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Print the name of the file in purple with ****** on both sides
        print("\033[95m****** Running tests in: ./testing/test_compare_dates.py ******\033[0m")
        cls.data = cls.load_original_data()

    @staticmethod
    def load_original_data(filename='output_data.json'):
        with open(filename, 'r') as file:
            return json.load(file)

    def test_compare_dates(self):
        mismatches = 0

        for group in self.data:
            for trial in group.get("nctNumbers", []):
                for nct_number, trial_data in trial.items():
                    original_date = trial_data["date"]
                    human_readable_date = trial_data["humanReadableDate"]

                    formatted_date = format_date(original_date)

                    with self.subTest(nct_number=nct_number):
                        if formatted_date != human_readable_date:
                            mismatches += 1
                            print(f"{COLOR_RED}Mismatch found for NCT number {nct_number}:{COLOR_RESET}")
                            print(f"{COLOR_GREEN}Original Date: {original_date}{COLOR_RESET}")
                            print(f"{COLOR_RED}Human-Readable Date: {human_readable_date}{COLOR_RESET}")
                        else:
                            print(f"{COLOR_GREEN}Date match for NCT number {nct_number}:{COLOR_RESET}")
                            print(f"{COLOR_GREEN}Original Date: {original_date} -> Human-Readable Date: {human_readable_date}{COLOR_RESET}")
                        self.assertEqual(
                            formatted_date, human_readable_date, 
                            f"Mismatch for NCT number {nct_number}: Original Date: {original_date} vs Human-Readable Date: {human_readable_date}"
                        )

        if mismatches == 0:
            print(f"{COLOR_GREEN}All dates match correctly.{COLOR_RESET}")
        else:
            print(f"{COLOR_RED}Total mismatches: {mismatches}{COLOR_RESET}")

if __name__ == "__main__":
    unittest.main()

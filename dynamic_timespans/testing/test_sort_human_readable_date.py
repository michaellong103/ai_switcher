import unittest
from datetime import datetime, timedelta
import json
import os

# Define CURRENT_DATE based on the data's context
CURRENT_DATE = datetime(2024, 7, 16)

def sort_by_human_readable_date(trials):
    """Sort trials by the 'humanReadableDate' field."""
    return sorted(trials, key=lambda x: datetime.strptime(x["humanReadableDate"], "%d %B %Y"))

class TestSortHumanReadableDate(unittest.TestCase):

    def setUp(self):
        print("\033[95m****** Running tests in: ./testing/test_sort_human_readable_date.py ******\033[0m")

        # Attempt to find the output_data.json file in multiple locations
        possible_paths = [
            '../output_data.json',                  # Parent directory of the testing directory
            './output_data.json',                   # Current directory
            os.path.abspath('../output_data.json'), # Absolute path from the current directory
            os.path.abspath('./output_data.json')   # Absolute path from within the dynamic_timespans directory
        ]

        file_path = None
        for path in possible_paths:
            if os.path.exists(path):
                file_path = path
                break

        if not file_path:
            print("\033[91mThe output_data.json file could not be found in any of the specified paths.\033[0m")
            raise FileNotFoundError("The output_data.json file could not be found in any of the specified paths.")

        with open(file_path, 'r') as file:
            self.data = json.load(file)

    def test_sort_by_human_readable_date(self):
        """Ensure the trials are sorted by humanReadableDate."""
        for group in self.data:
            trials = group["nctNumbers"]
            sorted_trials = sort_by_human_readable_date([trial[list(trial.keys())[0]] for trial in trials])

            # Verify that the trials are sorted correctly
            human_readable_dates = [datetime.strptime(trial["humanReadableDate"], "%d %B %Y") for trial in sorted_trials]
            try:
                self.assertEqual(human_readable_dates, sorted(human_readable_dates), f"Entries in {group['trialGroup']} are not sorted by 'humanReadableDate'.")
                print(f"\033[92mGroup {group['trialGroup']} sorted correctly by 'humanReadableDate'.\033[0m")
            except AssertionError as e:
                print(f"\033[91m{e}\033[0m")
                raise

    def test_human_readable_date_consistency(self):
        """Check if 'humanReadableDate' is consistent with 'date'."""
        for group in self.data:
            for trial in group["nctNumbers"]:
                trial_data = list(trial.values())[0]
                date_str = trial_data["date"]
                expected_human_readable_date = self.calculate_human_readable_date(date_str)

                # Verify that the humanReadableDate matches the expected value
                try:
                    self.assertEqual(trial_data["humanReadableDate"], expected_human_readable_date,
                                     f"Inconsistency found in {group['trialGroup']} for NCT {list(trial.keys())[0]}: expected {expected_human_readable_date}, got {trial_data['humanReadableDate']}")
                    print(f"\033[92mHuman-readable date consistency check passed for {list(trial.keys())[0]} in {group['trialGroup']}.\033[0m")
                except AssertionError as e:
                    print(f"\033[91m{e}\033[0m")
                    raise

    def test_days_until_end_consistency(self):
        """Ensure that 'daysUntilEnd' is correctly calculated from 'date'."""
        for group in self.data:
            for trial in group["nctNumbers"]:
                trial_data = list(trial.values())[0]
                date_str = trial_data["date"]
                parsed_date = self.parse_date(date_str)
                
                if parsed_date is None:
                    self.fail(f"\033[91mFailed to parse date '{date_str}' for NCT {list(trial.keys())[0]} in {group['trialGroup']}.\033[0m")

                actual_days_until_end = (parsed_date - CURRENT_DATE).days

                # Verify that the daysUntilEnd matches the calculated value
                try:
                    self.assertEqual(trial_data["daysUntilEnd"], actual_days_until_end,
                                     f"Mismatch in 'daysUntilEnd' for {group['trialGroup']} NCT {list(trial.keys())[0]}: expected {actual_days_until_end}, got {trial_data['daysUntilEnd']}")
                    print(f"\033[92mDays until end consistency check passed for {list(trial.keys())[0]} in {group['trialGroup']}.\033[0m")
                except AssertionError as e:
                    print(f"\033[91m{e}\033[0m")
                    raise

    def calculate_human_readable_date(self, date_str):
        """Helper function to calculate the expected human-readable date from a given date string."""
        if len(date_str) == 7:  # Format: YYYY-MM
            date = datetime.strptime(date_str, "%Y-%m")
            # Calculate the last day of the month
            next_month = date.replace(day=28) + timedelta(days=4)  # this will never fail
            last_day = next_month - timedelta(days=next_month.day)
            return last_day.strftime("%d %B %Y")
        elif len(date_str) == 10:  # Format: YYYY-MM-DD
            date = datetime.strptime(date_str, "%Y-%m-%d")
            return date.strftime("%d %B %Y")
        else:
            return "Unknown"

    def parse_date(self, date_str):
        """Helper function to parse a date string into a datetime object."""
        if len(date_str) == 7:  # Format: YYYY-MM
            date = datetime.strptime(date_str, "%Y-%m")
            # Calculate the last day of the month
            next_month = date.replace(day=28) + timedelta(days=4)  # this will never fail
            last_day = next_month - timedelta(days=next_month.day)
            return last_day
        elif len(date_str) == 10:  # Format: YYYY-MM-DD
            return datetime.strptime(date_str, "%Y-%m-%d")
        return None

if __name__ == '__main__':
    unittest.main()

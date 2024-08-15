# ./dynamic_phases/testing/test_nct_comparison.py

import unittest
import json
import os

class TestNCTComparison(unittest.TestCase):

    def setUp(self):
        # Print the name of the file in purple before each test
        print("\033[95mRunning tests in: ./testing/test_nct_comparison.py\033[0m")

        # Correct paths to the files to be tested
        self.output_data_path = os.path.join(os.path.dirname(__file__), '../../dynamic_timespans/output_data.json')
        self.dynamic_questions_input_path = os.path.join(os.path.dirname(__file__), '../../API_response/dynamic_questions_input.json')
        self.finaloutput_path = os.path.join(os.path.dirname(__file__), '../../API_response/finaloutput.json')
        self.dynamic_timespans_path = os.path.join(os.path.dirname(__file__), '../../dynamic_timespans/dynamic_timespans.json')
        self.phase_question_output_path = os.path.join(os.path.dirname(__file__), '../../API_response/phase_question_output.json')  # Fix this path

        # Print paths to verify correctness
        print(f"Path to output_data.json: {self.output_data_path}")
        print(f"Path to dynamic_questions_input.json: {self.dynamic_questions_input_path}")
        print(f"Path to finaloutput.json: {self.finaloutput_path}")
        print(f"Path to dynamic_timespans.json: {self.dynamic_timespans_path}")
        print(f"Path to phase_question_output.json: {self.phase_question_output_path}")

        

    def load_nct_numbers(self, filepath, is_output_data=False):
        with open(filepath, 'r') as file:
            data = json.load(file)
            if is_output_data:
                return self.extract_nct_numbers_from_output_data(data)
            else:
                return self.extract_nct_numbers_generic(data)

    def extract_nct_numbers_generic(self, data):
        # Function to recursively extract all NCT numbers from the data
        nct_numbers = set()

        if isinstance(data, dict):
            for key, value in data.items():
                if key in ['NCTNumbers', 'nctNumber', 'nctId']:
                    if isinstance(value, list):
                        nct_numbers.update(value)
                    else:
                        nct_numbers.add(value)
                else:
                    nct_numbers.update(self.extract_nct_numbers_generic(value))
        
        elif isinstance(data, list):
            for item in data:
                nct_numbers.update(self.extract_nct_numbers_generic(item))
        
        return nct_numbers

    def extract_nct_numbers_from_output_data(self, data):
        # Specifically handle the structure of output_data.json
        nct_numbers = set()
        if isinstance(data, list):
            for group in data:
                if 'nctNumbers' in group and isinstance(group['nctNumbers'], list):
                    for nct_dict in group['nctNumbers']:
                        if isinstance(nct_dict, dict):
                            nct_numbers.update(nct_dict.keys())
        return nct_numbers

    def compare_nct_sets(self, nct_sets):
        # Compare all sets and report any discrepancies
        all_ncts = set.union(*nct_sets.values())
        discrepancies = {}

        for name, nct_set in nct_sets.items():
            missing_in_others = all_ncts - nct_set
            if missing_in_others:
                discrepancies[name] = missing_in_others
        
        return discrepancies

    def color_text(self, text, color_code):
        """Helper function to color terminal output"""
        return f"\033[{color_code}m{text}\033[0m"

    def test_nct_consistency_across_files(self):
        # Load NCT numbers from each file
        nct_dynamic_questions_input = self.load_nct_numbers(self.dynamic_questions_input_path)
        nct_finaloutput = self.load_nct_numbers(self.finaloutput_path)
        nct_phase_question_output = self.load_nct_numbers(self.phase_question_output_path)
        nct_output_data = self.load_nct_numbers(self.output_data_path, is_output_data=True)
        nct_dynamic_timespans = self.load_nct_numbers(self.dynamic_timespans_path)

        nct_sets = {
            "dynamic_questions_input.json": nct_dynamic_questions_input,
            "finaloutput.json": nct_finaloutput,
            "phase_question_output.json": nct_phase_question_output,
            "output_data.json": nct_output_data,
            "dynamic_timespans.json": nct_dynamic_timespans
        }

        # Print NCT numbers for each file
        for name, nct_set in nct_sets.items():
            print(f"NCTs in {name}: {nct_set}")

        # Compare the NCT sets across all files
        discrepancies = self.compare_nct_sets(nct_sets)

        if discrepancies:
            for file_name, missing_ncts in discrepancies.items():
                print(self.color_text(f"NCT numbers missing in {file_name}: {missing_ncts}", '31'))  # Red for discrepancies
            self.fail(self.color_text("Discrepancies found between NCT numbers in different files.", '31'))
        else:
            print(self.color_text("No discrepancies found between NCT numbers in all files.", '32'))  # Green for success

if __name__ == '__main__':
    unittest.main()

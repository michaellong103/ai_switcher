# tests/test_clinical_trials_query.py

import os
import json
import unittest
from clinical_trials_query import main
from unittest.mock import patch
from contextlib import redirect_stdout

class ClinicalTrialsQueryTest(unittest.TestCase):
    # Initialize class variables for test summary
    total_tests = 0
    successful_tests = 0
    failed_tests = 0

    def setUp(self):
        # Define the directories for input and output
        self.input_dir = 'tests/test_inputs'
        self.output_dir = 'tests/test_outputs'
        self.main_input_file = 'tests/test_input_data.json'  # Main input JSON file

        # Ensure the input and output directories exist
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

        # Load input data from the main JSON file
        self.input_data = self.load_main_input_data()

        # Create individual input files if they don't exist
        self.create_input_files()

    def load_main_input_data(self):
        """
        Load the main input data from the specified JSON file.
        
        :return: List of input data dictionaries
        """
        with open(self.main_input_file, 'r') as f:
            return json.load(f)

    def create_input_files(self):
        """
        Create individual input JSON files from the main input data.
        """
        for i, data in enumerate(self.input_data):
            input_file_path = os.path.join(self.input_dir, f'input{i+1}.json')
            # Only create the file if it doesn't already exist
            if not os.path.exists(input_file_path):
                with open(input_file_path, 'w') as f:
                    json.dump(data, f, indent=2)

    def tearDown(self):
        # Optionally, clean up the output files after tests
        for file in os.listdir(self.output_dir):
            file_path = os.path.join(self.output_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def test_clinical_trials_query(self):
        # List of input files
        input_files = [f for f in os.listdir(self.input_dir) if f.endswith('.json')]

        # Process each input file
        for input_file in input_files:
            ClinicalTrialsQueryTest.total_tests += 1
            input_file_path = os.path.join(self.input_dir, input_file)
            output_file_name = f"output_{input_file}"
            output_file_path = os.path.join(self.output_dir, output_file_name)

            try:
                # Redirect output to suppress it
                with open(os.devnull, 'w') as devnull, redirect_stdout(devnull):
                    # Run the main function to test the query
                    main(input_file_path, output_file_path)

                # Check if the output file is created
                self.assertTrue(os.path.exists(output_file_path), f"Output file {output_file_name} was not created")

                # Verify the content of the output file
                with open(output_file_path, 'r') as f:
                    output_data = json.load(f)

                # Perform checks on the output data structure
                self.assertIsInstance(output_data, dict, "Output data is not a dictionary")
                self.assertIn('studies', output_data, f"Key 'studies' not found in output data for {output_file_name}")

                # Increment successful tests
                ClinicalTrialsQueryTest.successful_tests += 1

            except AssertionError as e:
                print(f"Test failed for input file {input_file}: {str(e)}")
                ClinicalTrialsQueryTest.failed_tests += 1

    @classmethod
    def tearDownClass(cls):
        # Print the summary of test results
        print("\nTest Summary:")
        print(f"Total tests run: {cls.total_tests}")
        print(f"Successful tests: {cls.successful_tests}")
        print(f"Failed tests: {cls.failed_tests}")
        if cls.failed_tests > 0:
            print("Some tests failed. Please check the logs above for details.")

if __name__ == '__main__':
    unittest.main()

# ./tests/test_api_query.py

import unittest
from unittest.mock import patch, mock_open
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from api_query import main as query_main

class TestQueryAPI(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"nct_number": "NCT12345678"}')
    @patch('api_client.query_clinical_trial_by_nct')
    @patch('api_json_handler.write_json')
    def test_query_clinical_trial_by_nct_main(self, mock_write_json, mock_query_clinical_trial_by_nct, mock_file):
        mock_query_clinical_trial_by_nct.return_value = {
            "studies": [
                {"brief_title": "Trial 1", "nct_id": "NCT12345678"},
                {"brief_title": "Trial 2", "nct_id": "NCT87654321"}
            ]
        }

        input_file = 'input_test_nct.json'
        output_file = 'output_test.json'

        query_main(input_file, output_file)

        expected_stats = {
            "number_of_trials": 2,
            "trial_names": ["Trial 1", "Trial 2"],
            "nct_numbers": "NCT12345678,NCT87654321"
        }
        mock_write_json.assert_called_once_with(expected_stats, output_file)

    @patch('builtins.open', new_callable=mock_open, read_data='{"Age": "50", "Gender": "Female", "Medical Condition": "Triple Negative Breast Cancer", "Location": "Seattle, WA"}')
    @patch('api_client.query_clinical_trials')
    @patch('api_json_handler.write_json')
    def test_query_clinical_trials_main(self, mock_write_json, mock_query_clinical_trials, mock_file):
        mock_query_clinical_trials.return_value = [
            {"brief_title": "Trial 1", "nct_id": "NCT12345678"},
            {"brief_title": "Trial 2", "nct_id": "NCT87654321"}
        ]

        input_file = 'input_test_multiple.json'
        output_file = 'output_test.json'

        query_main(input_file, output_file)

        expected_stats = {
            "number_of_trials": 2,
            "trial_names": ["Trial 1", "Trial 2"],
            "nct_numbers": "NCT12345678,NCT87654321"
        }
        mock_write_json.assert_called_once_with(expected_stats, output_file)

if __name__ == '__main__':
    unittest.main()

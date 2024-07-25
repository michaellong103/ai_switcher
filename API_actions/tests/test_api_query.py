# ./API_actions/tests/test_api_query.py

import unittest
from unittest.mock import patch, mock_open
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../api_actions')))

from api_query import main as query_main

class TestQueryAPI(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='{"query": "test"}')
    @patch('api_actions.api_client.query_clinical_trials')
    @patch('api_actions.api_json_handler.write_json')
    def test_query_clinical_trials_main(self, mock_write_json, mock_query_clinical_trials, mock_file):
        mock_query_clinical_trials.return_value = {"response": "data"}

        input_file = 'api_actions/input.json'
        output_file = 'api_actions/output.json'

        query_main(input_file, output_file)

        mock_query_clinical_trials.assert_called_once_with({"query": "test"})
        mock_write_json.assert_called_once_with({"response": "data"}, output_file)

    @patch('builtins.open', new_callable=mock_open, read_data='{"nct_number": "NCT12345678"}')
    @patch('api_actions.api_client.query_clinical_trial_by_nct')
    @patch('api_actions.api_json_handler.write_json')
    def test_query_clinical_trial_by_nct_main(self, mock_write_json, mock_query_clinical_trial_by_nct, mock_file):
        mock_query_clinical_trial_by_nct.return_value = {"response": "data"}

        input_file = 'api_actions/input.json'
        output_file = 'api_actions/output.json'

        query_main(input_file, output_file)

        mock_query_clinical_trial_by_nct.assert_called_once_with("NCT12345678")
        mock_write_json.assert_called_once_with({"response": "data"}, output_file)

if __name__ == '__main__':
    unittest.main()

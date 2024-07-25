# ./API_actions/tests/test_api_client.py

import unittest
from unittest.mock import patch
from api_actions.api_client import query_clinical_trials, query_clinical_trial_by_nct

class TestApiClient(unittest.TestCase):
    @patch('api_actions.api_client.requests.post')
    @patch('api_actions.api_client.time.sleep', return_value=None)  # Mock time.sleep to avoid delay in tests
    def test_query_clinical_trials(self, mock_sleep, mock_post):
        mock_response = mock_post.return_value
        mock_response.json.return_value = {"key": "value"}

        details = {
            'Age': '50', 
            'Gender': 'Female', 
            'Medical Condition': 'Triple Negative Breast Cancer', 
            'Location': 'Seattle, WA'
        }
        response = query_clinical_trials(details)
        self.assertEqual(response, {"key": "value"})
        mock_sleep.assert_called_once_with(1)  # Ensure the sleep was called

    @patch('api_actions.api_client.requests.get')
    @patch('api_actions.api_client.time.sleep', return_value=None)  # Mock time.sleep to avoid delay in tests
    def test_query_clinical_trial_by_nct(self, mock_sleep, mock_get):
        mock_response = mock_get.return_value
        mock_response.json.return_value = {"key": "value"}

        nct_number = "NCT12345678"
        response = query_clinical_trial_by_nct(nct_number)
        self.assertEqual(response, {"key": "value"})
        mock_sleep.assert_called_once_with(1)  # Ensure the sleep was called

if __name__ == '__main__':
    unittest.main()

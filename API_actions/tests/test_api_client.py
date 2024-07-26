# ./tests/test_api_client.py

import unittest
from unittest.mock import patch
from api_client import query_clinical_trials, query_clinical_trial_by_nct

class TestApiClient(unittest.TestCase):
    @patch('api_client.requests.post')
    @patch('api_client.time.sleep', return_value=None)  # Mock time.sleep to avoid delay in tests
    def test_query_clinical_trials(self, mock_sleep, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 200  # Ensure the status code is 200
        mock_response.json.side_effect = [
            {"studies": [{"brief_title": "Trial 1", "nct_id": "NCT12345678"}], "nextCursor": "cursor1"},
            {"studies": [{"brief_title": "Trial 2", "nct_id": "NCT87654321"}], "nextCursor": None}
        ]
        
        details = {
            'Age': '50', 
            'Gender': 'Female', 
            'Medical Condition': 'Triple Negative Breast Cancer', 
            'Location': 'Seattle, WA',
            'Latitude': '47.6062',
            'Longitude': '-122.3321',
            'Distance': '100'
        }
        response = query_clinical_trials(details)
        self.assertEqual(response, [
            {"brief_title": "Trial 1", "nct_id": "NCT12345678"},
            {"brief_title": "Trial 2", "nct_id": "NCT87654321"}
        ])
        mock_sleep.assert_called()  # Ensure the sleep was called at least once

    @patch('api_client.requests.post')
    @patch('api_client.time.sleep', return_value=None)  # Mock time.sleep to avoid delay in tests
    def test_query_clinical_trial_by_nct(self, mock_sleep, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 200  # Ensure the status code is 200
        mock_response.json.return_value = {"studies": [{"brief_title": "Trial 1", "nct_id": "NCT12345678"}]}
        
        nct_number = "NCT12345678"
        response = query_clinical_trial_by_nct(nct_number)
        self.assertEqual(response, {"studies": [{"brief_title": "Trial 1", "nct_id": "NCT12345678"}]})
        mock_sleep.assert_called()  # Ensure the sleep was called at least once

if __name__ == '__main__':
    unittest.main()

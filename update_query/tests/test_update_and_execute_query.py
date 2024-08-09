import unittest
from unittest.mock import patch, mock_open
import json
import os
from update_query.update_and_execute_query import (
    read_config_state,
    update_search_radius_km,
    save_updated_config_and_query,
    execute_api_query
)

class TestUpdateAndExecuteQuery(unittest.TestCase):
    
    @patch('builtins.open', new_callable=mock_open, read_data='{"search_radius_km": 100}')
    def test_read_config_state(self, mock_file):
        config = read_config_state('config_state.json')
        self.assertIsNotNone(config)
        self.assertEqual(config['search_radius_km'], 100)

    def test_update_search_radius_km(self):
        config_state = {'search_radius_km': 100}
        new_radius = update_search_radius_km(config_state)
        self.assertEqual(new_radius, 150)
        self.assertEqual(config_state['search_radius_km'], 150)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.makedirs')
    def test_save_updated_config_and_query(self, mock_makedirs, mock_file):
        config_state = {
            'search_radius_km': 100,
            'last_clinical_trials_api_url': 'http://example.com/api',
            'current_api_params': {}
        }
        save_updated_config_and_query(config_state, 'config_state.json')
        mock_file.assert_called_with('config_state.json', 'w')
        self.assertEqual(config_state['search_radius_km'], 150)

    @patch('update_query.update_and_execute_query.clinical_trials_query_main')
    @patch('os.makedirs')
    def test_execute_api_query(self, mock_makedirs, mock_query):
        mock_query.return_value = None  # Simulate successful query execution
        status_code, message = execute_api_query()
        self.assertEqual(status_code, 0)
        self.assertIn('API query executed successfully', message)

if __name__ == '__main__':
    unittest.main()

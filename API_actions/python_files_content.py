# ./python_files_content.py

import sys
import os
import json
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from api_client import query_clinical_trials, query_clinical_trial_by_nct
from api_json_handler import read_json, write_json

def process_api_response(api_response):
    # Extract required information from API response
    if isinstance(api_response, dict) and 'studies' in api_response:
        studies = api_response['studies']
    elif isinstance(api_response, list):
        studies = api_response
    else:
        studies = []

    num_trials = len(studies)
    trial_names = [study.get('brief_title', 'N/A') for study in studies]
    nct_numbers = [study.get('nct_id', 'N/A') for study in studies]

    stats = {
        "number_of_trials": num_trials,
        "trial_names": trial_names,
        "nct_numbers": ",".join(nct_numbers)
    }

    # Log the details
    logging.info(f"Number of trials: {num_trials}")
    logging.info(f"Trial names: {trial_names}")

    return stats

def log_query_details(query_details, stats, log_file='query_log.json'):
    log_data = {
        "query_details": query_details,
        "stats": stats
    }
    with open(log_file, 'a') as file:
        json.dump(log_data, file, indent=4)
        file.write("\n")

def main(input_file, output_file):
    logging.info(f"Reading from: {input_file}")
    logging.info(f"Writing to: {output_file}")

    # Read input JSON
    input_data = read_json(input_file)

    if 'nct_number' in input_data:
        # Query a single clinical trial based on NCT number
        api_response = query_clinical_trial_by_nct(input_data['nct_number'])
    else:
        # Query multiple clinical trials
        api_response = query_clinical_trials(input_data)

    # Process API response to extract statistics
    stats = process_api_response(api_response)

    # Log and write the query details to a JSON file
    log_query_details(input_data, stats)

    # Write the stats to the output JSON
    write_json(stats, output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python api_query.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)

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

import unittest
import json
from api_actions.api_json_handler import read_json, write_json

class TestJsonHandler(unittest.TestCase):
    def test_read_json(self):
        with open('test_input.json', 'w') as file:
            json.dump({"key": "value"}, file)

        data = read_json('test_input.json')
        self.assertEqual(data, {"key": "value"})

    def test_write_json(self):
        data = {"key": "value"}
        write_json(data, 'test_output.json')

        with open('test_output.json', 'r') as file:
            result = json.load(file)
        
        self.assertEqual(result, data)

if __name__ == '__main__':
    unittest.main()

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

import json

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

import sys
import os
import json
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from api_client import query_clinical_trials, query_clinical_trial_by_nct
from api_json_handler import read_json, write_json

def process_api_response(api_response):
    # Extract required information from API response
    if isinstance(api_response, dict) and 'studies' in api_response:
        studies = api_response['studies']
    elif isinstance(api_response, list):
        studies = api_response
    else:
        studies = []

    num_trials = len(studies)
    trial_names = [study.get('brief_title', 'N/A') for study in studies]
    nct_numbers = [study.get('nct_id', 'N/A') for study in studies]

    stats = {
        "number_of_trials": num_trials,
        "trial_names": trial_names,
        "nct_numbers": ",".join(nct_numbers)
    }

    # Log the details
    logging.info(f"Number of trials: {num_trials}")
    logging.info(f"Trial names: {trial_names}")

    return stats

API_ENDPOINT_CLINICAL_TRIALS = "https://clinicaltrials.gov/api/v2/studies"

import requests
import time
import logging
from api_config import API_ENDPOINT_CLINICAL_TRIALS
from urllib.parse import urlencode

class ClinicalTrialsAPI:
    def __init__(self, page_size=200, status_filter="RECRUITING|NOT_YET_RECRUITING|AVAILABLE"):
        self.page_size = page_size
        self.status_filter = status_filter

    def send_query_to_clinicaltrials(self, details, distance):
        details["Distance"] = str(distance)
        all_studies = []
        cursor = None

        while True:
            query_url = self.construct_query_url(details, self.status_filter, self.page_size, cursor)

            response = requests.get(query_url)
            if response.status_code == 200:
                data = response.json()
                studies = data.get('studies', [])
                all_studies.extend(studies)

                cursor = data.get('nextCursor')
                if not cursor:
                    break
            else:
                logging.error(f"Error {response.status_code}: {response.text}")
                break

            # Ensure at least a 1 second pause between API calls
            time.sleep(1)

        return all_studies

    def construct_query_url(self, details, status_filter, page_size, cursor=None):
        condition = details.get("Medical Condition", "")
        gender = details.get("Gender", "").lower()
        latitude = details.get("Latitude", "")
        longitude = details.get("Longitude", "")
        distance = details.get("Distance", "100")

        geo_filter = f"distance({latitude},{longitude},{distance})"

        query_params = {
            "format": "json",
            "query.cond": condition,
            "filter.geo": geo_filter,
            "aggFilters": f"sex:{gender[0]}",
            "filter.overallStatus": status_filter,
            "pageSize": page_size
        }

        if cursor:
            query_params["nextCursor"] = cursor

        query_string = urlencode(query_params, safe="(),|")
        query_url = f"{API_ENDPOINT_CLINICAL_TRIALS}?{query_string}"
        
        return query_url

def query_clinical_trials(details):
    api = ClinicalTrialsAPI()
    return api.send_query_to_clinicaltrials(details, details.get("Distance", 100))

def query_clinical_trial_by_nct(nct_number):
    url = f"{API_ENDPOINT_CLINICAL_TRIALS}/{nct_number}?format=json"
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Ensure at least a 1 second pause between API calls
    time.sleep(1)
    
    response = requests.get(url, headers=headers)
    return response.json()

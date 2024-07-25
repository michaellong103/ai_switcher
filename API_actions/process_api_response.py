# ./process_api_response.py

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

# ./api_query.py

import sys
import os
import json
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from api_client import query_clinical_trials, query_clinical_trial_by_nct
from api_json_handler import read_json, write_json

def process_api_response(api_response):
    # Extract required information from API response
    studies = []
    if isinstance(api_response, dict) and 'studies' in api_response:
        studies = api_response['studies']
    elif isinstance(api_response, list):
        studies = api_response

    num_trials = len(studies)
    trial_names = []
    nct_numbers = []

    for study in studies:
        protocol_section = study.get('protocolSection', {})
        identification_module = protocol_section.get('identificationModule', {})
        
        brief_title = identification_module.get('briefTitle', 'N/A')
        nct_id = identification_module.get('nctId', 'N/A')
        
        trial_names.append(brief_title)
        nct_numbers.append(nct_id)

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

def clear_log_file(log_file='query_log.json'):
    # Clear the log file at the beginning of the script
    open(log_file, 'w').close()

def main(input_file, output_file):
    logging.info(f"Reading from: {input_file}")
    logging.info(f"Writing to: {output_file}")

    # Clear the log file
    clear_log_file()

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

    # Log the query details to a JSON file
    log_query_details(input_data, stats)

    # Write the raw API response to the output JSON
    write_json(api_response, output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python api_query.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)

# api_query.py

import sys
import os
import json
import logging

# Initialize logging configuration
logging.basicConfig(
    level=logging.CRITICAL,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_query.log'),
        logging.StreamHandler()
    ]
)

# Ensure the path is set for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Import necessary functions from other modules
from api_client import query_clinical_trials, query_clinical_trial_by_nct
from api_json_handler import read_json, write_json
from data_cleaning import clean_study_data, extract_clinical_trial_info, filter_exclusion_criteria_and_write, save_all_study_data

def process_api_response(api_response):
    logging.debug("Processing API response")
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
    logging.debug(f"Extracted stats: {stats}")

    return stats

def log_query_details(query_details, stats, log_file='query_log.json'):
    logging.debug(f"Logging query details to {log_file}")
    log_data = {
        "query_details": query_details,
        "stats": stats
    }
    with open(log_file, 'a') as file:
        json.dump(log_data, file, indent=4)
        file.write("\n")

def clear_log_file(log_file='query_log.json'):
    logging.debug(f"Clearing log file: {log_file}")
    # Clear the log file at the beginning of the script
    open(log_file, 'w').close()

def main(input_file, output_file):
    logging.info(f"Reading from: {input_file}")
    logging.info(f"Writing to: {output_file}")

    # Clear the log file
    clear_log_file()

    # Read input JSON
    logging.debug("Reading input JSON")
    input_data = read_json(input_file)
    logging.debug(f"Input data: {input_data}")

    if 'nct_number' in input_data:
        # Query a single clinical trial based on NCT number
        logging.info("Querying single clinical trial by NCT number")
        api_response = query_clinical_trial_by_nct(input_data['nct_number'])
    else:
        # Query multiple clinical trials
        logging.info("Querying multiple clinical trials")
        api_response = query_clinical_trials(input_data)

    logging.debug(f"API response: {api_response}")

    # Process API response to extract statistics
    stats = process_api_response(api_response)

    # Log the query details to a JSON file
    log_query_details(input_data, stats)

    # Write the raw API response to the output JSON
    write_json(api_response, output_file)

    # Extract output directory from the output file path
    output_dir = os.path.dirname(output_file)
    logging.debug(f"Output directory: {output_dir}")

    # Call data cleaning functions
    extracted_data = extract_clinical_trial_info(api_response, output_dir)
    logging.debug(f"Extracted data: {extracted_data}")
    cleaned_data = clean_study_data(api_response, output_dir)
    logging.debug(f"Cleaned data: {cleaned_data}")
    filter_exclusion_criteria_and_write(cleaned_data, output_dir)
    save_all_study_data(api_response, output_dir)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python api_query.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)

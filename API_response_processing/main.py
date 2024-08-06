# main.py

import os
import logging
from typing import Dict

try:
    from .data_cleaning import clean_study_data, filter_exclusion_criteria_and_write
    from .data_extraction import extract_clinical_trial_info
    from .file_utils import load_json_from_file, save_json_to_file
except ImportError:
    from data_cleaning import clean_study_data, filter_exclusion_criteria_and_write
    from data_extraction import extract_clinical_trial_info
    from file_utils import load_json_from_file, save_json_to_file

def process_clinical_trials(input_json_file: str, output_dir: str):
    """
    Processes clinical trial data by extracting and cleaning relevant information.

    Args:
        input_json_file (str): Path to the input JSON file containing trial data.
        output_dir (str): Directory to save the processed data.
    """
    # Load the trial data from the JSON file
    data = load_json_from_file(input_json_file)

    if data is None:
        logging.error("Failed to load data from the input JSON file.")
        return

    # Ensure the data is structured correctly
    if 'studies' not in data:
        logging.error("The input JSON does not contain the 'studies' key.")
        return

    trials_data = data['studies']
    logging.info(f"Loaded {len(trials_data)} trials from input file.")

    # Extract information from the trial data
    extract_clinical_trial_info(trials_data, output_dir)

    # Clean the study data
    cleaned_data = clean_study_data(trials_data, output_dir)

    # Filter exclusion criteria and write filtered data
    filter_exclusion_criteria_and_write(cleaned_data, output_dir)

    # Save all study data to a JSON file
    all_data_file_path = os.path.join(output_dir, 'all_study_data.json')
    save_json_to_file(trials_data, all_data_file_path, "All data")

if __name__ == "__main__":
    # Hardcoded paths
    input_json_file = "../API_response/finaloutput.json"
    output_dir = "../API_response"

    # Resolve absolute paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_json_file = os.path.join(script_dir, input_json_file)
    output_dir = os.path.join(script_dir, output_dir)

    # Set up logging
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    process_clinical_trials(input_json_file, output_dir)

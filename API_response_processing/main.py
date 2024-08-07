# ./API_response_processing/main.py

import os
import logging
import sys
from typing import List, Dict, Any

try:
    from .data_cleaning import clean_study_data, filter_exclusion_criteria_and_write
    from .data_extraction import extract_clinical_trial_info
    from .info_extraction import extract_condensed_info, extract_detailed_info  # Added imports
    from .file_utils import load_json_from_file, save_json_to_file
except ImportError:
    from data_cleaning import clean_study_data, filter_exclusion_criteria_and_write
    from data_extraction import extract_clinical_trial_info
    from info_extraction import extract_condensed_info, extract_detailed_info  # Added imports
    from file_utils import load_json_from_file, save_json_to_file


def process_clinical_trials(input_json_file: str, output_dir: str) -> None:
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

    # Extract condensed information from the trial data
    extract_condensed_info(trials_data, output_dir)  # Added condensed info extraction

    # Extract detailed information from the trial data
    extract_detailed_info(trials_data, output_dir)  # Added detailed info extraction

    # Clean the study data
    cleaned_data = clean_study_data(trials_data, output_dir)

    # Filter exclusion criteria and write filtered data
    filter_exclusion_criteria_and_write(cleaned_data, output_dir)

    # Save all study data to a JSON file
    all_data_file_path = os.path.join(output_dir, 'all_study_data.json')
    save_json_to_file(trials_data, all_data_file_path, "All data")


def main() -> None:
    """
    Main function to execute the clinical trials processing workflow.
    """
    # Set up logging configuration
    logging.basicConfig(
        level=logging.INFO,  # Set to DEBUG to see detailed logs
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("api_response_processing.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Define input and output paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_json_file = os.path.join(script_dir, "../API_response/finaloutput.json")
    output_dir = os.path.join(script_dir, "../API_response")

    # Check if input JSON file exists
    if not os.path.exists(input_json_file):
        logging.error(f"Input JSON file not found: {input_json_file}")
        sys.exit(1)

    # Create output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Start the processing
    logging.info("Starting clinical trials data processing.")
    process_clinical_trials(input_json_file, output_dir)
    logging.info("Completed clinical trials data processing.")


if __name__ == "__main__":
    main()

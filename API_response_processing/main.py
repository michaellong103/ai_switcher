# ./main.py
import os
import logging
import sys
from typing import List, Dict, Any

try:
    from .data_cleaning import clean_study_data, filter_exclusion_criteria_and_write
    from .data_extraction import extract_clinical_trial_info
    from .info_extraction import extract_condensed_info, extract_detailed_info
    from .file_utils import load_json_from_file, save_json_to_file
    from .clinical_trial_processor import run_processing  # Importing run_processing
except ImportError:
    from data_cleaning import clean_study_data, filter_exclusion_criteria_and_write
    from data_extraction import extract_clinical_trial_info
    from info_extraction import extract_condensed_info, extract_detailed_info
    from file_utils import load_json_from_file, save_json_to_file
    from clinical_trial_processor import run_processing  # Importing run_processing

def process_clinical_trials(input_json_file: str, output_dir: str) -> None:
    data = load_json_from_file(input_json_file)
    if data is None:
        logging.error('Failed to load data from the input JSON file.')
        return
    if 'studies' not in data:
        logging.error("The input JSON does not contain the 'studies' key.")
        return
    trials_data = data['studies']
    logging.info(f'Loaded {len(trials_data)} trials from input file.')
    extract_clinical_trial_info(trials_data, output_dir)
    extract_condensed_info(trials_data, output_dir)
    extract_detailed_info(trials_data, output_dir)
    cleaned_data = clean_study_data(trials_data, output_dir)
    filter_exclusion_criteria_and_write(cleaned_data, output_dir)
    all_data_file_path = os.path.join(output_dir, 'all_study_data.json')
    save_json_to_file(trials_data, all_data_file_path, 'All data')

def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_json_file = os.path.join(script_dir, '../API_response/finaloutput.json')
    output_dir = os.path.join(script_dir, '../API_response')
    if not os.path.exists(input_json_file):
        logging.error(f'Input JSON file not found: {input_json_file}')
        sys.exit(1)
    os.makedirs(output_dir, exist_ok=True)
    logging.info('Starting clinical trials data processing.')

    # Run the processing from clinical_trial_processor
    run_processing()

    process_clinical_trials(input_json_file, output_dir)
    logging.info('Completed clinical trials data processing.')

if __name__ == '__main__':
    main()

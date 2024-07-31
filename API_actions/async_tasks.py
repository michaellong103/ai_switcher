# ./API_actions/async_tasks.py
import os
import logging
from api_client import query_clinical_trials, query_clinical_trial_by_nct
from api_json_handler import read_json, write_json
from response_processor import process_api_response
from log_utils import log_query_details, clear_log_file
from data_cleaning import clean_study_data, extract_clinical_trial_info, filter_exclusion_criteria_and_write, save_all_study_data
from output_sort import sort_and_process_trials

async def async_main(input_file, output_file):
    logging.info(f"Reading from: {input_file}")
    logging.info(f"Writing to: {output_file}")

    clear_log_file()

    try:
        logging.debug("Reading input JSON")
        input_data = read_json(input_file)
        logging.debug(f"Input data: {input_data}")
    except FileNotFoundError:
        logging.error(f"The input file '{input_file}' does not exist.")
        return None
    except Exception as e:
        logging.error(f"Error reading input JSON: {e}", exc_info=True)
        return None

    try:
        if 'nct_number' in input_data:
            logging.info("Querying single clinical trial by NCT number")
            api_response = await query_clinical_trial_by_nct(input_data['nct_number'])
        else:
            logging.info("Querying multiple clinical trials")
            api_response = await query_clinical_trials(input_data)

        logging.debug(f"API response: {api_response}")

        stats = process_api_response(api_response)
        log_query_details(input_data, stats)
        write_json(api_response, output_file)

        output_dir = os.path.dirname(output_file)
        logging.debug(f"Output directory: {output_dir}")

        extracted_data = extract_clinical_trial_info(api_response, output_dir)
        logging.debug(f"Extracted data: {extracted_data}")
        cleaned_data = clean_study_data(api_response, output_dir)
        logging.debug(f"Cleaned data: {cleaned_data}")
        filter_exclusion_criteria_and_write(cleaned_data, output_dir)
        save_all_study_data(api_response, output_dir)

        logging.info("Sorting and processing trials")
        result_type = sort_and_process_trials(stats['number_of_trials'])
        logging.info(f"Result of sorting: {result_type}")

        return api_response

    except Exception as e:
        logging.error(f"Error in async_main: {e}", exc_info=True)
        return None

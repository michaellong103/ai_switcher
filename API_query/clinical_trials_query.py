# ./API_query/clinical_trials_query.py
import os
import json
import requests
import sys
import logging
try:
    from .query_logger import log_query
    from .update_stats import update_stats_from_response
except ImportError as e:
    logging.warning(f'Relative import failed: {e}')
    from query_logger import log_query
    from update_stats import update_stats_from_response
try:
    from API_response_processing.main import main as process_api_response
    from API_response_evaluation.main import main as evaluate_trials
except ImportError as e:
    logging.warning(f'Initial import failed: {e}')
    from .API_response_processing.main import main as process_api_response
    from .API_response_evaluation.main import main as evaluate_trials

def load_input(file_path):
    logging.debug(f'Loading input file from: {file_path}')
    if not os.path.exists(file_path):
        logging.error(f'Input file not found: {file_path}')
        raise FileNotFoundError(f'Input file not found: {file_path}')
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            logging.info(f'Input data loaded from {file_path}')
            return data
    except json.JSONDecodeError as e:
        logging.error(f'JSON decode error: {e}')
        raise

def construct_query_url(data, default_radius=10):
    logging.debug(f'Constructing query URL with data: {data} and default_radius: {default_radius}')
    radius = data.get('Radius', default_radius)
    base_url = 'https://clinicaltrials.gov/api/v2/studies'
    params = {'format': 'json', 'query.cond': data['Medical Condition'].replace(' ', '+'), 'pageSize': 200, 'filter.overallStatus': 'RECRUITING|NOT_YET_RECRUITING|AVAILABLE', 'filter.geo': f'distance({data['Latitude']},{data['Longitude']},{radius})'}
    query_url = f'{base_url}?{'&'.join((f'{key}={value}' for key, value in params.items()))}'
    log_query(query_url, data)
    logging.info(f'Constructed query URL: {query_url}')
    return query_url

def update_config_state(input_data, config_file_path, query_url, radius):
    updated_data = {'current_api_params': input_data, 'search_radius_km': radius, 'last_clinical_trials_api_url': query_url, 'stats': {'number_of_trials': 0, 'trial_names': [], 'nct_numbers': ''}}
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as config_file:
            config_data = json.load(config_file)
    else:
        config_data = {}
    config_data.update(updated_data)
    with open(config_file_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    logging.info('Config state updated successfully.')

def fetch_clinical_trials(query_url):
    try:
        logging.info(f'Fetching data from API: {query_url}')
        response = requests.get(query_url, timeout=10)
        response.raise_for_status()
        logging.info('Data fetched successfully from the API.')
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f'HTTP error occurred: {http_err}')
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f'Connection error occurred: {conn_err}')
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f'Timeout error occurred: {timeout_err}')
    except requests.exceptions.RequestException as req_err:
        logging.error(f'An error occurred: {req_err}')
    return None

def extract_nct_ids(response_data):
    logging.debug('Extracting NCT IDs from response data...')
    nct_ids = []
    if 'studies' in response_data:
        for study in response_data['studies']:
            if 'nctId' in study['protocolSection']['identificationModule']:
                nct_ids.append(study['protocolSection']['identificationModule']['nctId'])
    if nct_ids:
        logging.info(f'Extracted NCT IDs: {", ".join(nct_ids)}')
    else:
        logging.warning('Query returned no studies or no NCT IDs found.')
    return nct_ids

def save_output(data, file_path):
    logging.debug(f'Saving output data to: {file_path}')
    try:
        dir_name = os.path.dirname(file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        logging.info(f'Data successfully saved to {file_path}')
    except IOError as e:
        logging.error(f'Failed to write output data to {file_path}: {e}')
        raise

def check_file_path(file_path):
    logging.debug(f'Checking if file path exists: {file_path}')
    if os.path.exists(file_path):
        logging.info(f"The file '{file_path}' exists.")
    else:
        logging.error(f"The file '{file_path}' does not exist.")

def main():
    logging.info('Starting Clinical Trials Query Process')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, 'input.json')
    output_file_path_1 = os.path.join(script_dir, 'output.json')
    output_file_path_2 = os.path.join(script_dir, '..', 'API_response', 'finaloutput.json')
    logging.debug('Checking file paths...')
    logging.debug('Checking input file path...')
    check_file_path(input_file_path)
    logging.debug('Checking output file path 1...')
    check_file_path(output_file_path_1)
    logging.debug('Checking output file path 2...')
    check_file_path(output_file_path_2)
    try:
        input_data = load_input(input_file_path)
        logging.info('Input data loaded successfully.')
    except FileNotFoundError as e:
        logging.error(e)
        sys.exit(1)
    except json.JSONDecodeError as e:
        logging.error(f'JSON decode error: {e}')
        sys.exit(1)
    query_url = construct_query_url(input_data)
    config_file_path = os.path.join(script_dir, '..', 'config_state.json')
    update_config_state(input_data, config_file_path, query_url, input_data.get('Radius', 10))
    clinical_trials_data = fetch_clinical_trials(query_url)
    if clinical_trials_data:
        update_stats_from_response(clinical_trials_data, config_file_path)
        save_output(clinical_trials_data, output_file_path_1)
        save_output(clinical_trials_data, output_file_path_2)
        logging.info(f'Results saved to {output_file_path_1} and {output_file_path_2}')
        logging.info('Executing the API response processing.')
        process_api_response()
        logging.info('Executing the API response evaluation.')
        evaluate_trials()
        logging.info('Finished executing the API response evaluation.')
    else:
        logging.error('Failed to fetch clinical trials data.')
if __name__ == '__main__':
    logging.debug('Starting main function.')
    main()
    logging.debug('Finished executing main function.')

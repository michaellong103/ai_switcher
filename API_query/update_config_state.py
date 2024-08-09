# ./API_query/update_config_state.py
import json
import os
import logging
import sys

def load_input(file_path):
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

def construct_query_url(data, radius=100):
    base_url = 'https://clinicaltrials.gov/api/v2/studies'
    params = {'format': 'json', 'query.cond': data['Medical Condition'].replace(' ', '+'), 'filter.geo': f'distance({data['Latitude']},{data['Longitude']},{radius})', 'aggFilters': f'sex%3A{data['Gender'][0].lower()}', 'filter.overallStatus': 'RECRUITING|NOT_YET_RECRUITING|AVAILABLE', 'pageSize': 200}
    query_url = f'{base_url}?{'&'.join((f'{key}={value}' for key, value in params.items()))}'
    return query_url

def update_config_state(input_data, config_file_path, radius=100):
    query_url = construct_query_url(input_data, radius)
    updated_data = {'current_api_params': input_data, 'search_radius_km': radius, 'last_clinical_trials_api_url': query_url, 'stats': {'number_of_trials': 0, 'trial_names': [], 'nct_numbers': ''}}
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as config_file:
            config_data = json.load(config_file)
    else:
        config_data = {}
    config_data.update(updated_data)
    with open(config_file_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print('Config state updated successfully.')

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, 'input.json')
    config_file_path = os.path.join(script_dir, '..', 'config_state.json')
    try:
        input_data = load_input(input_file_path)
        logging.info('Input data loaded successfully.')
    except FileNotFoundError as e:
        logging.error(e)
        sys.exit(1)
    except json.JSONDecodeError as e:
        logging.error(f'JSON decode error: {e}')
        sys.exit(1)
    update_config_state(input_data, config_file_path)
if __name__ == '__main__':
    main()

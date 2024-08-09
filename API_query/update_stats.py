# ./API_query/update_stats.py
import json
import os
import logging
import sys

def load_config_state(config_file_path):
    if not os.path.exists(config_file_path):
        logging.error(f'Config file not found: {config_file_path}')
        raise FileNotFoundError(f'Config file not found: {config_file_path}')
    try:
        with open(config_file_path, 'r') as f:
            data = json.load(f)
            logging.info(f'Config data loaded from {config_file_path}')
            return data
    except json.JSONDecodeError as e:
        logging.error(f'JSON decode error: {e}')
        raise

def update_stats_from_response(response_data, config_file_path):
    try:
        studies = response_data.get('studies', [])
        number_of_trials = len(studies)
        trial_names = []
        nct_numbers = []
        for study in studies:
            try:
                nct_id = study['protocolSection']['identificationModule']['nctId']
                brief_title = study['protocolSection']['identificationModule']['briefTitle']
                nct_numbers.append(nct_id)
                trial_names.append(brief_title)
            except KeyError as e:
                logging.warning(f'Missing expected key in study data: {e}')
                continue
        config_data = load_config_state(config_file_path)
        config_data['stats'] = {'number_of_trials': number_of_trials, 'trial_names': trial_names, 'nct_numbers': ', '.join(nct_numbers)}
        save_config_state(config_data, config_file_path)
        logging.info('Stats section updated successfully.')
    except Exception as e:
        logging.error(f'Failed to update stats: {e}')
        raise

def save_config_state(config_data, config_file_path):
    try:
        with open(config_file_path, 'w') as f:
            json.dump(config_data, f, indent=4)
        logging.info(f'Config data saved to {config_file_path}')
    except IOError as e:
        logging.error(f'Failed to write config data to {config_file_path}: {e}')
        raise

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_dir, '..', 'config_state.json')
    response_data = {'studies': [{'protocolSection': {'identificationModule': {'nctId': 'NCT05491226', 'briefTitle': 'Reinvigorating TNBC Response to Immunotherapy With Combination Myeloid Inhibition and Radiation'}}}]}
    update_stats_from_response(response_data, config_file_path)
if __name__ == '__main__':
    main()

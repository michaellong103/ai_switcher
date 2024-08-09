# ./update_query/update_and_execute_query.py
import os
import json
import logging
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.insert(0, parent_dir)

from API_query.clinical_trials_query import main as clinical_trials_query_main

def read_config_state(config_file_path):
    """Reads the current state from config_state.json."""
    try:
        with open(config_file_path, 'r') as file:
            config_state = json.load(file)
        return config_state
    except FileNotFoundError:
        logging.error(f'Error: {config_file_path} not found.')
        return None
    except json.JSONDecodeError as e:
        logging.error(f'Error decoding JSON from {config_file_path}: {e}')
        return None

def update_search_radius_km(config_state, increment=50):
    """Updates the search radius by a given increment."""
    if 'search_radius_km' in config_state:
        config_state['search_radius_km'] += increment
    else:
        config_state['search_radius_km'] = increment
    return config_state['search_radius_km']

def save_updated_config_and_query(config_state, config_file_path):
    """Constructs the query URL, updates the config state, and saves it."""
    search_radius_km = update_search_radius_km(config_state)

    query_url = config_state['last_clinical_trials_api_url']  # Assuming it needs to be reused
    
    config_state['current_api_params']['Radius'] = search_radius_km
    
    with open(config_file_path, 'w') as config_file:
        json.dump(config_state, config_file, indent=4)
    logging.info(f'Config state updated with new query URL and search radius {search_radius_km} km.')

    input_file_path = os.path.join(os.path.dirname(config_file_path), 'API_query', 'input.json')
    with open(input_file_path, 'w') as input_file:
        json.dump(config_state['current_api_params'], input_file, indent=4)
    logging.info(f'Updated API query parameters saved to {input_file_path}')

def execute_api_query():
    """Triggers the API query process."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, '..', 'API_query', 'input.json')
    output_file_path = os.path.join(script_dir, '..', 'API_response', 'output_final_big.json')
    
    logging.info(f'Executing API query with input_file: {input_file_path}, output_file: {output_file_path}')
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    try:
        clinical_trials_query_main()
        logging.info('The API query is complete, and the files have been written successfully.')
        return (0, 'API query executed successfully.')
    except Exception as e:
        logging.error(f'There was an issue with the API query: {e}')
        return (1, f'Error executing API query: {e}')

def main():
    """Main function to update search radius, save query, and trigger the API call."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_dir, '..', 'config_state.json')
    
    config_state = read_config_state(config_file_path)
    if not config_state:
        return
    
    save_updated_config_and_query(config_state, config_file_path)
    
    execute_api_query()

if __name__ == '__main__':
    main()

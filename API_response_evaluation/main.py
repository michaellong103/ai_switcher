import os
import json
import logging
try:
    logging.debug("Attempting to import 'evaluate_trials' functions.")
    from evaluate_trials import load_config, load_trials_data, evaluate_number_of_trials
    logging.info("Successfully imported 'evaluate_trials' functions from the same directory.")
except ImportError:
    logging.debug("Failed to import 'evaluate_trials' functions from the same directory. Attempting relative import.")
    from .evaluate_trials import load_config, load_trials_data, evaluate_number_of_trials
    logging.info("Successfully imported 'evaluate_trials' functions using relative import.")

def load_config_state(config_state_path):
    logging.debug(f'Loading config state from: {config_state_path}')
    try:
        if os.path.exists(config_state_path):
            with open(config_state_path, 'r') as file:
                config_state = json.load(file)
                logging.info(f'Config state loaded successfully from {config_state_path}')
                return config_state
        else:
            logging.warning(f'Config state file does not exist: {config_state_path}. Returning default state.')
            return {'current_api_params': {}, 'last_clinical_trials_api_url': '', 'stats': {}}
    except json.JSONDecodeError as e:
        logging.error(f'Failed to decode JSON from the config state file: {e}')
        raise

def update_config_state(config_state_path, trials, response):
    logging.debug(f'Updating config state at: {config_state_path}')
    try:
        config_state = load_config_state(config_state_path)
        config_state['API_response_evaluation'] = response
        with open(config_state_path, 'w') as file:
            json.dump(config_state, file, indent=4)
        logging.info('Config state updated successfully.')
    except Exception as e:
        logging.error(f'Error updating config state: {e}')
        print(f"Error: Unable to update the config state in '{config_state_path}'.")

def main():
    logging.info('Starting API response evaluation process')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_dir, 'config.json')
    final_output_path = os.path.join(script_dir, '..', 'API_response', 'finaloutput.json')
    config_state_path = os.path.join(script_dir, '..', 'config_state.json')
    try:
        logging.debug(f'Loading configuration from: {config_file_path}')
        config = load_config(config_file_path)
        logging.info('Configuration loaded successfully.')
    except Exception as e:
        logging.error(f'Error loading configuration: {e}')
        print(f"Error: Unable to load the configuration file '{config_file_path}'. Please ensure it exists and is properly formatted.")
        return
    try:
        logging.debug(f'Loading trials data from: {final_output_path}')
        trials = load_trials_data(final_output_path)
        logging.info(f'Loaded {len(trials)} trials from the final output file.')
    except FileNotFoundError as e:
        logging.error(f'Final output file not found: {e}')
        print(f"Error: The required input file '{final_output_path}' was not found. Please generate the file and try again.")
        return
    except Exception as e:
        logging.error(f'Error loading trial data: {e}')
        print(f"Error: Unable to load trial data from '{final_output_path}'. Please ensure the file exists and is properly formatted.")
        return
    try:
        logging.debug('Evaluating the number of trials')
        response = evaluate_number_of_trials(trials, config)
        logging.info('Evaluation completed successfully.')
        print(response)
    except Exception as e:
        logging.error(f'Error during trial evaluation: {e}')
        print('Error: Unable to evaluate the number of trials.')
        return
    logging.debug('Updating config state with evaluation response')
    update_config_state(config_state_path, trials, response)
if __name__ == '__main__':
    logging.debug('Starting main function.')
    main()
    logging.debug('Finished executing main function.')

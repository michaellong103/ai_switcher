# ./API_response_evaluation/evaluate_trials.py
import json
import logging
from event_system import event_system

logging.info('Starting evaluate_trials.py')

try:
    from .display_in_terminal.main import run_main
    logging.info('Imported run_main from .display_in_terminal.main')
except ImportError as e:
    logging.error(f'Failed to import run_main from .display_in_terminal.main: {e}')
    try:
        from display_in_terminal.main import run_main
        logging.info('Imported run_main from display_in_terminal.main')
    except ImportError as e:
        logging.error(f'Failed to import run_main from display_in_terminal.main: {e}')
        try:
            from ..display_in_terminal.main import run_main
            logging.info('Imported run_main from ..display_in_terminal.main')
        except ImportError as e:
            logging.error(f'Failed to import run_main from ..display_in_terminal.main: {e}')
            raise ImportError('Unable to import run_main from any known locations')

def load_config(config_path):
    logging.info('Starting load_config function')
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            logging.info('Configuration loaded successfully')
            return config
    except FileNotFoundError as e:
        logging.error(f'Configuration file not found: {e}')
        raise
    except json.JSONDecodeError as e:
        logging.error(f'Failed to decode JSON from the configuration file: {e}')
        raise
    finally:
        logging.info('Finished load_config function')

def load_trials_data(final_output_path):
    logging.info('Starting load_trials_data function')
    try:
        with open(final_output_path, 'r') as file:
            data = json.load(file)
            logging.info('Trial data loaded successfully')
            return data.get('studies', [])
    except FileNotFoundError as e:
        logging.error(f'Final output file not found: {e}')
        raise
    except json.JSONDecodeError as e:
        logging.error(f'Failed to decode JSON from the final output file: {e}')
        raise
    finally:
        logging.info('Finished load_trials_data function')

def evaluate_number_of_trials(trials, config):
    logging.info('Starting evaluate_number_of_trials function')

    num_trials = len(trials)
    if num_trials == config['no_trials']:
        logging.info("No trials found, emitting NO_TRIALS_FOUND event.")
        event_system.emit('NO_TRIALS_FOUND')
        result = 'No trials'
    elif num_trials < config['a_lot_of_trials']:
        result = 'Few trials'
        run_main('detailed')
    elif num_trials < config['too_many_trials']:
        result = 'A lot of trials'
        run_main('condensed')
    else:
        result = 'Too many trials'
    logging.info(f'Evaluation result: {result}')
    logging.info('Finished evaluate_number_of_trials function')
    return result

def main():
    logging.info('Executing evaluate_trials main process')
    config_path = 'API_response_evaluation/config.json'
    final_output_path = 'API_response/finaloutput.json'
    config = load_config(config_path)
    trials = load_trials_data(final_output_path)
    evaluation_result = evaluate_number_of_trials(trials, config)
    logging.info(f'Evaluation result: {evaluation_result}')
    if evaluation_result == 'Few trials':
        logging.info("Calling run_main with 'detailed'")
    elif evaluation_result == 'A lot of trials':
        logging.info("Calling run_main with 'condensed'")
    logging.info('Finished executing evaluate_trials.py')

if __name__ == '__main__':
    main()

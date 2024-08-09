import json
import logging
logger = logging.getLogger(__name__)
logger.info('Starting evaluate_trials.py')
try:
    from .display_in_terminal.main import run_main
    logger.info('Imported run_main from .display_in_terminal.main')
except ImportError as e:
    logger.error(f'Failed to import run_main from .display_in_terminal.main: {e}')
    try:
        from display_in_terminal.main import run_main
        logger.info('Imported run_main from display_in_terminal.main')
    except ImportError as e:
        logger.error(f'Failed to import run_main from display_in_terminal.main: {e}')
        try:
            from ..display_in_terminal.main import run_main
            logger.info('Imported run_main from ..display_in_terminal.main')
        except ImportError as e:
            logger.error(f'Failed to import run_main from ..display_in_terminal.main: {e}')
            raise ImportError('Unable to import run_main from any known locations')

def load_config(config_path):
    logger.info('Starting load_config function')
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            logger.info('Configuration loaded successfully')
            return config
    except FileNotFoundError as e:
        logger.error(f'Configuration file not found: {e}')
        raise
    except json.JSONDecodeError as e:
        logger.error(f'Failed to decode JSON from the configuration file: {e}')
        raise
    finally:
        logger.info('Finished load_config function')

def load_trials_data(final_output_path):
    logger.info('Starting load_trials_data function')
    try:
        with open(final_output_path, 'r') as file:
            data = json.load(file)
            logger.info('Trial data loaded successfully')
            return data.get('studies', [])
    except FileNotFoundError as e:
        logger.error(f'Final output file not found: {e}')
        raise
    except json.JSONDecodeError as e:
        logger.error(f'Failed to decode JSON from the final output file: {e}')
        raise
    finally:
        logger.info('Finished load_trials_data function')

def evaluate_number_of_trials(trials, config):
    logger.info('Starting evaluate_number_of_trials function')
    num_trials = len(trials)
    if num_trials == config['no_trials']:
        result = 'No trials'
    elif num_trials < config['a_lot_of_trials']:
        result = 'Few trials'
        run_main('detailed')
    elif num_trials < config['too_many_trials']:
        result = 'A lot of trials'
        run_main('condensed')
    else:
        result = 'Too many trials'
    logger.info(f'Evaluation result: {result}')
    logger.info('Finished evaluate_number_of_trials function')
    return result

def main():
    logger.info('Executing evaluate_trials main process')
    config_path = 'API_response_evaluation/config.json'
    final_output_path = 'API_response/finaloutput.json'
    config = load_config(config_path)
    trials = load_trials_data(final_output_path)
    evaluation_result = evaluate_number_of_trials(trials, config)
    logger.info(f'Evaluation result: {evaluation_result}')
    if evaluation_result == 'Few trials':
        logger.info("Calling run_main with 'detailed'")
    elif evaluation_result == 'A lot of trials':
        logger.info("Calling run_main with 'condensed'")
    else:
        logger.info(f'Evaluation result: {evaluation_result}')
    logger.info('Finished executing evaluate_trials.py')
if __name__ == '__main__':
    main()

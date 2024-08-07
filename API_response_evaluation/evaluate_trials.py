# evaluate_trials.py

import json
import logging
from display_in_terminal.main import run_main

def load_config(config_path):
    """
    Load the configuration settings from a JSON file.

    Args:
        config_path (str): Path to the configuration JSON file.

    Returns:
        dict: Configuration data as a dictionary.
    """
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            return config
    except FileNotFoundError as e:
        logging.error(f"Configuration file not found: {e}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON from the configuration file: {e}")
        raise

def load_trials_data(final_output_path):
    """
    Load trial data from the final output JSON file.

    Args:
        final_output_path (str): Path to the finaloutput.json file.

    Returns:
        list: List of trials data.
    """
    try:
        with open(final_output_path, 'r') as file:
            data = json.load(file)
            return data.get("studies", [])
    except FileNotFoundError as e:
        logging.error(f"Final output file not found: {e}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON from the final output file: {e}")
        raise

def evaluate_number_of_trials(trials, config):
    """
    Evaluate the number of trials and return the appropriate response.

    Args:
        trials (list): List of trials data.
        config (dict): Configuration data with thresholds.

    Returns:
        str: Response based on the number of trials.
    """
    num_trials = len(trials)

    if num_trials == config["no_trials"]:
        return "No trials"
    elif num_trials < config["a_lot_of_trials"]:
        return "Few trials"
    elif num_trials < config["too_many_trials"]:
        return "A lot of trials"
    else:
        return "Too many trials"

def execute_main_script(display_type, json_path):
    """
    Directly call the run_main function from main.py.

    Args:
        display_type (str): The display type to be used.
        json_path (str): The path to the JSON file.
    """
    run_main(display_type, json_path)

def main():
    # Load the configuration and trial data
    config_path = "API_response_evaluation/config.json"
    final_output_path = "API_response/finaloutput.json"

    config = load_config(config_path)
    trials = load_trials_data(final_output_path)

    # Evaluate the number of trials
    evaluation_result = evaluate_number_of_trials(trials, config)

    # Execute the main script with the appropriate arguments
    if evaluation_result == "Few trials":
        execute_main_script("condensed", final_output_path)
    elif evaluation_result == "A lot of trials":
        execute_main_script("detailed", final_output_path)
    else:
        print(f"Evaluation result: {evaluation_result}")

if __name__ == "__main__":
    main()

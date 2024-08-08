# ./API_response_evaluation/main.py

import os
import json
import logging

# Import the main functions from evaluate_trials with extensive logging
try:
    logging.debug("Attempting to import 'evaluate_trials' functions.")
    from evaluate_trials import load_config, load_trials_data, evaluate_number_of_trials
    logging.info("Successfully imported 'evaluate_trials' functions from the same directory.")
except ImportError:
    logging.debug("Failed to import 'evaluate_trials' functions from the same directory. Attempting relative import.")
    from .evaluate_trials import load_config, load_trials_data, evaluate_number_of_trials
    logging.info("Successfully imported 'evaluate_trials' functions using relative import.")

def load_config_state(config_state_path):
    """
    Load the current state from config_state.json.

    Args:
        config_state_path (str): Path to the config_state.json file.

    Returns:
        dict: Configuration state data as a dictionary.
    """
    logging.debug(f"Loading config state from: {config_state_path}")
    try:
        if os.path.exists(config_state_path):
            with open(config_state_path, 'r') as file:
                config_state = json.load(file)
                logging.info(f"Config state loaded successfully from {config_state_path}")
                return config_state
        else:
            logging.warning(f"Config state file does not exist: {config_state_path}. Returning default state.")
            # Return an empty structure if the file does not exist
            return {"current_api_params": {}, "last_clinical_trials_api_url": "", "stats": {}}
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON from the config state file: {e}")
        raise

def update_config_state(config_state_path, trials, response):
    """
    Update the config_state.json with the evaluation response.

    Args:
        config_state_path (str): Path to the config_state.json file.
        trials (list): List of trials data.
        response (str): Evaluation response string.

    Returns:
        None
    """
    logging.debug(f"Updating config state at: {config_state_path}")
    try:
        # Load the existing config state
        config_state = load_config_state(config_state_path)

        # Only update the parts you want to change, preserving "stats"
        config_state["API_response_evaluation"] = response

        # You can update other fields here if needed, but not "stats"
        # config_state["some_other_field"] = some_value

        # Write the updated config state back to the file
        with open(config_state_path, 'w') as file:
            json.dump(config_state, file, indent=4)
        
        logging.info("Config state updated successfully.")
    except Exception as e:
        logging.error(f"Error updating config state: {e}")
        print(f"Error: Unable to update the config state in '{config_state_path}'.")

def main():
    logging.info("Starting API response evaluation process")
    
    # Calculate absolute paths based on the current script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_dir, "config.json")
    final_output_path = os.path.join(script_dir, "..", "API_response", "finaloutput.json")
    config_state_path = os.path.join(script_dir, "..", "config_state.json")

    # Load configuration settings
    try:
        logging.debug(f"Loading configuration from: {config_file_path}")
        config = load_config(config_file_path)
        logging.info("Configuration loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        print(f"Error: Unable to load the configuration file '{config_file_path}'. Please ensure it exists and is properly formatted.")
        return

    # Load trial data from finaloutput.json
    try:
        logging.debug(f"Loading trials data from: {final_output_path}")
        trials = load_trials_data(final_output_path)
        logging.info(f"Loaded {len(trials)} trials from the final output file.")
    except FileNotFoundError as e:
        logging.error(f"Final output file not found: {e}")
        print(f"Error: The required input file '{final_output_path}' was not found. Please generate the file and try again.")
        return
    except Exception as e:
        logging.error(f"Error loading trial data: {e}")
        print(f"Error: Unable to load trial data from '{final_output_path}'. Please ensure the file exists and is properly formatted.")
        return

    # Evaluate the number of trials and print the result
    try:
        logging.debug("Evaluating the number of trials")
        response = evaluate_number_of_trials(trials, config)
        logging.info("Evaluation completed successfully.")
        print(response)
    except Exception as e:
        logging.error(f"Error during trial evaluation: {e}")
        print("Error: Unable to evaluate the number of trials.")
        return

    # Update the config_state.json with the evaluation response
    logging.debug("Updating config state with evaluation response")
    update_config_state(config_state_path, trials, response)

if __name__ == "__main__":
    logging.debug("Starting main function.")
    main()
    logging.debug("Finished executing main function.")

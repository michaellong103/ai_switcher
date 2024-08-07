# ./main.py

import os
import json
import logging


try:
    # Import the main function from API_response_processing
    from evaluate_trials import load_config, load_trials_data, evaluate_number_of_trials
except ImportError:
    from .evaluate_trials import load_config, load_trials_data, evaluate_number_of_trials

def load_config_state(config_state_path):
    """
    Load the current state from config_state.json.

    Args:
        config_state_path (str): Path to the config_state.json file.

    Returns:
        dict: Configuration state data as a dictionary.
    """
    try:
        if os.path.exists(config_state_path):
            with open(config_state_path, 'r') as file:
                return json.load(file)
        else:
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
    # Calculate absolute paths based on the current script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_dir, "config.json")
    final_output_path = os.path.join(script_dir, "..", "API_response", "finaloutput.json")
    config_state_path = os.path.join(script_dir, "..", "config_state.json")

    # Load configuration settings
    try:
        config = load_config(config_file_path)
        logging.info("Configuration loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        print(f"Error: Unable to load the configuration file '{config_file_path}'. Please ensure it exists and is properly formatted.")
        return

    # Load trial data from finaloutput.json
    try:
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
    response = evaluate_number_of_trials(trials, config)
    print(response)

    # Update the config_state.json with the evaluation response
    update_config_state(config_state_path, trials, response)

if __name__ == "__main__":
    # Start the main process
    main()

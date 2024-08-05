# ./update_stats.py

import json
import os
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Use DEBUG for detailed output
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("clinical_trials_query.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def load_config_state(config_file_path):
    """
    Load data from the config_state.json file.

    :param config_file_path: Path to the config_state.json file
    :return: Data extracted from the JSON file as a dictionary
    """
    if not os.path.exists(config_file_path):
        logging.error(f"Config file not found: {config_file_path}")
        raise FileNotFoundError(f"Config file not found: {config_file_path}")

    try:
        with open(config_file_path, 'r') as f:
            data = json.load(f)
            logging.info(f"Config data loaded from {config_file_path}")
            return data
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        raise

def update_stats(config_data, number_of_trials, trial_names, nct_numbers):
    """
    Update the stats section in the config data.

    :param config_data: Existing config data as a dictionary
    :param number_of_trials: Number of trials to update
    :param trial_names: List of trial names to update
    :param nct_numbers: String of NCT numbers to update
    """
    config_data["stats"] = {
        "number_of_trials": number_of_trials,
        "trial_names": trial_names,
        "nct_numbers": nct_numbers
    }
    logging.info("Stats section updated successfully.")

def save_config_state(config_data, config_file_path):
    """
    Save the updated config data back to the config_state.json file.

    :param config_data: Updated config data as a dictionary
    :param config_file_path: Path to the config_state.json file
    """
    try:
        with open(config_file_path, 'w') as f:
            json.dump(config_data, f, indent=4)
        logging.info(f"Config data saved to {config_file_path}")
    except IOError as e:
        logging.error(f"Failed to write config data to {config_file_path}: {e}")
        raise

def main():
    # Calculate absolute path based on the current script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_dir, "..", "config_state.json")

    # Load existing config data
    try:
        config_data = load_config_state(config_file_path)
        logging.info("Config data loaded successfully.")
    except FileNotFoundError as e:
        logging.error(e)
        sys.exit(1)
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        sys.exit(1)

    # Update the stats section with new data
    number_of_trials = 5  # Example value, replace with actual data
    trial_names = ["Trial A", "Trial B", "Trial C", "Trial D", "Trial E"]  # Example list
    nct_numbers = "NCT001, NCT002, NCT003, NCT004, NCT005"  # Example NCT numbers

    update_stats(config_data, number_of_trials, trial_names, nct_numbers)

    # Save the updated config data back to the file
    save_config_state(config_data, config_file_path)

if __name__ == "__main__":
    main()

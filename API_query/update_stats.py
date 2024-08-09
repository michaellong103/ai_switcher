# ./update_stats.py

import json
import os
import logging
import sys



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

def update_stats_from_response(response_data, config_file_path):
    """
    Update the stats section in the config_state.json file with data from the API response.

    :param response_data: The JSON response data from the API
    :param config_file_path: Path to the config_state.json file
    """
    try:
        # Extract trial information from the API response
        studies = response_data.get("studies", [])
        number_of_trials = len(studies)
        trial_names = []
        nct_numbers = []

        for study in studies:
            try:
                # Extract nctId and briefTitle for each study
                nct_id = study["protocolSection"]["identificationModule"]["nctId"]
                brief_title = study["protocolSection"]["identificationModule"]["briefTitle"]

                nct_numbers.append(nct_id)
                trial_names.append(brief_title)
            except KeyError as e:
                logging.warning(f"Missing expected key in study data: {e}")
                continue

        # Load the existing config data
        config_data = load_config_state(config_file_path)

        # Update the stats section in the config data
        config_data["stats"] = {
            "number_of_trials": number_of_trials,
            "trial_names": trial_names,
            "nct_numbers": ', '.join(nct_numbers)
        }

        # Save the updated config data back to the file
        save_config_state(config_data, config_file_path)

        logging.info("Stats section updated successfully.")
    except Exception as e:
        logging.error(f"Failed to update stats: {e}")
        raise

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

    # Example response data, replace with actual API response
    response_data = {
      "studies": [
        {
          "protocolSection": {
            "identificationModule": {
              "nctId": "NCT05491226",
              "briefTitle": "Reinvigorating TNBC Response to Immunotherapy With Combination Myeloid Inhibition and Radiation"
            }
          }
        },
        # Add more studies as needed
      ]
    }

    # Update the stats section with data from the response
    update_stats_from_response(response_data, config_file_path)

if __name__ == "__main__":
    main()

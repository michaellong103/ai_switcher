# ./API_query/update_config_state.py

import json
import os
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,  # Use DEBUG for more detailed output
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("clinical_trials_query.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def load_input(file_path):
    """
    Load input data from a JSON file.

    :param file_path: Path to the input JSON file
    :return: Data extracted from the JSON file as a dictionary
    """
    if not os.path.exists(file_path):
        logging.error(f"Input file not found: {file_path}")
        raise FileNotFoundError(f"Input file not found: {file_path}")

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            logging.info(f"Input data loaded from {file_path}")
            return data
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        raise

def construct_query_url(data, radius=100):
    """
    Construct a query URL for the clinical trials API.

    :param data: Dictionary containing input parameters
    :param radius: Radius for the location search in kilometers
    :return: Constructed query URL as a string
    """
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "format": "json",
        "query.cond": data["Medical Condition"].replace(" ", "+"),
        "filter.geo": f"distance({data['Latitude']},{data['Longitude']},{radius})",
        "aggFilters": f"sex%3A{data['Gender'][0].lower()}",
        "filter.overallStatus": "RECRUITING|NOT_YET_RECRUITING|AVAILABLE",
        "pageSize": 200
    }

    query_url = f"{base_url}?{'&'.join(f'{key}={value}' for key, value in params.items())}"
    return query_url

def update_config_state(input_data, config_file_path):
    """
    Update the config_state.json file with current API parameters and query URL.

    :param input_data: Data extracted from the input JSON file
    :param config_file_path: Path to the config_state.json file
    """
    # Construct the query URL using input data
    query_url = construct_query_url(input_data)

    # Define the data to be updated in the config state
    updated_data = {
        "current_api_params": input_data,
        "last_clinical_trials_api_url": query_url,
        "stats": {
            "number_of_trials": 0,  # Placeholder, update with real data if available
            "trial_names": [],      # Placeholder, update with real data if available
            "nct_numbers": ""       # Placeholder, update with real data if available
        }
    }

    # Load the existing config state if it exists
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as config_file:
            config_data = json.load(config_file)
    else:
        config_data = {}

    # Update the config state with new data
    config_data.update(updated_data)

    # Write the updated config state back to the file
    with open(config_file_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)

    logging.info("Config state updated successfully.")

def main():
    # Calculate absolute paths based on the current script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, "input.json")

    # Path for config_state.json
    config_file_path = os.path.join(script_dir, "..", "config_state.json")

    # Load input data from the input JSON file
    try:
        input_data = load_input(input_file_path)
        logging.info("Input data loaded successfully.")
    except FileNotFoundError as e:
        logging.error(e)
        sys.exit(1)
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        sys.exit(1)

    # Update the config state with the input data and query URL
    update_config_state(input_data, config_file_path)

if __name__ == "__main__":
    main()

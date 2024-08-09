import os
import json
import logging
import sys
import time  # Import time for adding delays

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.insert(0, parent_dir)

from config import start_distance, max_distance, increase_radius_distance
from write_input_json import write_to_input_json
from API_query.clinical_trials_query import main as clinical_trials_query_main  # Import the clinical trials query function

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config_state():
    try:
        # Path to config_state.json in the parent directory
        config_file_path = os.path.join(parent_dir, 'config_state.json')
        
        logging.info(f"Loading config state from {config_file_path}")
        
        # Load the JSON data from the config file
        with open(config_file_path, 'r') as file:
            config_data = json.load(file)
        
        logging.debug(f"Config data loaded: {config_data}")
        return config_data
    
    except FileNotFoundError:
        logging.error(f"config_state.json not found at {config_file_path}")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from config_state.json: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    
    return None

def increase_radius(current_radius):
    """Increase the radius by increase_radius_distance but do not exceed max_distance."""
    new_radius = current_radius + increase_radius_distance
    if new_radius > max_distance:
        new_radius = max_distance
    logging.info(f"Radius increased to: {new_radius} km (max: {max_distance} km)")
    return new_radius

def execute_api_query():
    input_file_path = './API_query/input.json'
    output_file_path = './API_response/output_final_big.json'
    logging.info(f'Executing API query with input_file: {input_file_path}, output_file: {output_file_path}')
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    try:
        clinical_trials_query_main()  # Execute the clinical trials query
        logging.info('The API query is complete, and the files have been written successfully.')
        return (0, 'API query executed successfully.')
    except Exception as e:
        logging.error(f'There was an issue with the API query: {e}')
        return (1, f'Error executing API query: {e}')

def main():
    # Load the config state data
    config_data = load_config_state()
    
    if config_data:
        # Extract the necessary fields
        age = config_data.get("current_api_params", {}).get("Age", "")
        gender = config_data.get("current_api_params", {}).get("Gender", "")
        medical_condition = config_data.get("current_api_params", {}).get("Medical Condition", "")
        location = config_data.get("current_api_params", {}).get("Location", "")
        latitude = config_data.get("current_api_params", {}).get("Latitude", "")
        longitude = config_data.get("current_api_params", {}).get("Longitude", "")
        
        # Determine the distance to use: from current_api_params or search_radius_km
        if "Distance" in config_data.get("current_api_params", {}):
            current_radius = config_data["current_api_params"]["Distance"]
            logging.info(f"Using Distance from current_api_params: {current_radius} km")
        else:
            current_radius = config_data.get("search_radius_km", start_distance)
            logging.info(f"Using Distance from search_radius_km: {current_radius} km")
        
        # Increase the radius but respect the max_distance
        new_radius = increase_radius(current_radius)

        # Write the updated radius and other data to input.json
        write_to_input_json(age, gender, medical_condition, location, latitude, longitude, new_radius)

        # Update the config state with the new radius
        if "Distance" in config_data.get("current_api_params", {}):
            config_data["current_api_params"]["Distance"] = new_radius
        else:
            config_data["search_radius_km"] = new_radius
        
        with open(os.path.join(parent_dir, 'config_state.json'), 'w') as file:
            json.dump(config_data, file, indent=4)
        logging.info(f"Config state updated with new radius: {new_radius} km")
        
        # Pause for 2 seconds before running the API query
        time.sleep(2)

        # Execute the API query after updating the input.json
        result_code, result_message = execute_api_query()
        logging.info(result_message)
    else:
        logging.error("Failed to load data from config_state.json. Aborting the process.")

if __name__ == "__main__":
    main()

# ./API_actions/increase_radius.py
import json
import sys
import os
import logging

logger = logging.getLogger(__name__)

def increase_radius(config_file):
    try:
        # Check if the configuration file exists
        if not os.path.exists(config_file):
            logger.error(f"Configuration file '{config_file}' does not exist.")
            return
        
        # Load the configuration file
        with open(config_file, 'r') as file:
            config = json.load(file)
        
        # Ensure location exists in the configuration
        location = config.get("current_api_params", {}).get("Location", "unknown location")
        
        # Increase the radius by 50 miles
        current_radius = config.get("current_radius_for_search", 0)
        new_radius = current_radius + 50
        config["current_radius_for_search"] = new_radius
        
        # Print the location and the new search radius
        print(f"Location: {location}")
        print(f"Increasing search radius to {new_radius} miles.")
        logger.info(f"Radius increased from {current_radius} miles to {new_radius} miles for {location}.")
        
        # Save the updated configuration back to the file
        with open(config_file, 'w') as file:
            json.dump(config, file, indent=4)
        logger.info(f"Updated configuration saved to '{config_file}'.")

    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from file {config_file}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python increase_radius.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    increase_radius(config_file)

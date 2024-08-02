# ./API_actions/output_sort.py

import logging
import json
import sys
import os
import time  # Import time for delay

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from display_in_terminal.main import main as display_main

display_types = ["condensed", "detailed", "questions"]
json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../API_response/output_final_big.json'))
STATE_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config_state.json'))

logger = logging.getLogger(__name__)

def create_zero_result_file():
    """Creates a file named zero_result.txt when no trials are found."""
    zero_result_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'zero_result.txt'))
    with open(zero_result_file_path, 'w') as file:
        file.write("No clinical trials found for the given criteria.")
    logger.info("Created zero_result.txt as no trials were found.")

def no_trials_found(location, initial_distance):
    """
    Increases the search distance iteratively until it reaches 600 miles.
    If no trials are found at each step, a message is printed indicating the failure.
    Updates the current_radius_for_search in config_state.json as the distance expands.

    Parameters:
    - location (str): The location where the trials are searched.
    - initial_distance (int): The starting search distance in miles.

    Returns:
    str: A final message indicating the search status.
    """
    distance = initial_distance
    max_distance = 600
    trials_found = False  # Mock variable to simulate trials not being found

    while not trials_found and distance <= max_distance:
        # Simulate a search delay of 2 seconds between attempts
        logger.info(f"Searching for trials in {location} at {distance} miles...")
        time.sleep(2)

        # Simulate a search result check (this is a mockup, replace with actual logic if needed)
        trials_found = simulate_search_for_trials(location, distance)

        # Print message for each iteration
        print(f"No trials found in {location} at {distance} miles. Increasing distance...")

        if trials_found:
            logger.info(f"Trials found in {location} at {distance} miles.")
            print(f"Trials found in {location} at {distance} miles.")
            return f"Trials found in {location} at {distance} miles."

        # Update the search radius in the state file
        update_search_radius_in_state_file(distance)

        logger.info(f"No trials found in {location} at {distance} miles. Increasing distance...")
        distance += 50

    # If no trials found even at max distance, log the result
    final_message = f"No trials found in {location} up to {max_distance} miles.\n"
    final_message += f"\n{MAROON}Consider modifying your search criteria, such as trying a different location or condition.{RESET}\n"
    logger.info(final_message)
    print(final_message)
    return final_message

def update_search_radius_in_state_file(new_radius):
    """
    Updates the current_radius_for_search in config_state.json with the new_radius.

    Parameters:
    - new_radius (int): The new search radius to update in the state file.
    """
    try:
        # Load the current state from the state file
        with open(STATE_FILE_PATH, 'r') as state_file:
            state_data = json.load(state_file)

        # Update the current_radius_for_search
        state_data['current_radius_for_search'] = new_radius

        # Save the updated state back to the state file
        with open(STATE_FILE_PATH, 'w') as state_file:
            json.dump(state_data, state_file, indent=4)

        logger.info(f"Updated current_radius_for_search to {new_radius} in config_state.json.")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error while updating radius: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while updating radius: {e}", exc_info=True)

def simulate_search_for_trials(location, distance):
    """
    Simulate the search for trials. This is a placeholder function that always returns False.

    Parameters:
    - location (str): The location where the trials are searched.
    - distance (int): The search distance in miles.

    Returns:
    bool: Whether trials were found or not.
    """
    # This mock function always returns False, replace with actual trial search logic if available
    return False

def sort_and_process_trials(num_trials, location="Unknown", initial_distance=100):
    """Sort and process trials based on the number of trials found."""
    logger.info(f"Number of trials found: {num_trials}")
    print(f"Number of trials found: {num_trials}")

    # Output text messages for each scenario
    if num_trials > 20:
        logger.info("Too many trials found. Number of trials is greater than 20.")
        print("Too many trials found. Number of trials is greater than 20.")
        return 'There are too many trials found. Consider refining your search criteria.'

    elif num_trials == 0:
        logger.info("No trials found. Number of trials is 0.")
        create_zero_result_file()  # Create zero_result.txt

        # Log information that no trials were found and call no_trials_found to handle increasing distance
        logger.info("No trials found.")

        # Directly return the no_trials_found message to ensure print during loop execution
        return no_trials_found(location, initial_distance)

    elif 1 <= num_trials <= 5:
        logger.info("Few trials found. Number of trials is between 1 and 5. Detailed output.")
        print("Few trials found. Detailed output.")
        display_main("detailed", json_path)
        return 'A few trials were found. Displaying detailed information.'

    elif 6 <= num_trials <= 20:
        logger.info("A moderate number of trials found. Number of trials is between 6 and 20. Condensed output.")
        print("A moderate number of trials found. Condensed output.")
        display_main("condensed", json_path)
        return 'A moderate number of trials were found. Displaying condensed information.'

    else:
        logger.error(f"No sort worked. The number of trials does not make sense. Number of trials: {num_trials}")
        print("No sort worked. The number of trials does not make sense.")
        return 'An error occurred while processing trials. Please try again.'

def main(stats_file):
    """Main function to process the stats file and sort trials."""
    logger.info(f"Starting output_sort.py with stats_file: {stats_file}")

    if not os.path.exists(stats_file):
        logger.error(f"Error: The stats file '{stats_file}' does not exist.")
        print(f"Error: The stats file '{stats_file}' does not exist.")
        sys.exit(1)

    try:
        with open(stats_file, 'r') as file:
            stats = json.load(file)
        num_trials = stats.get('number_of_trials', 0)
        location = stats.get('location', 'Unknown')  # Assume location is passed in stats for use
        initial_distance = stats.get('distance', 100)  # Assume distance is passed in stats for use
        logger.info(f"Sorting and processing {num_trials} trials for location {location}")

        # Capture the result text
        result_text = sort_and_process_trials(num_trials, location, initial_distance)
        logger.debug(f"Result text: {result_text}")

        # Return the result text for use by external callers
        return result_text
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
        print(f"JSON decoding error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("Usage: python output_sort.py <stats_file>")
        print("Usage: python output_sort.py <stats_file>")
        sys.exit(1)
    
    stats_file = sys.argv[1]
    main(stats_file)

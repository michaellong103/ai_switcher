# ./API_actions/output_sort.py
import logging
import json
import sys
import os
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from display_in_terminal.main import main as display_main

display_types = ["condensed", "detailed", "questions"]
json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../API_response/output_final_big.json'))
STATE_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config_state.json'))

logger = logging.getLogger(__name__)

def sort_and_process_trials(num_trials):
    # Log the number of trials found
    logger.info(f"Number of trials found: {num_trials}")
    print(f"Number of trials found: {num_trials}")

    if num_trials > 20:
        logger.info("Too many trials found. Number of trials is greater than 20.")
        print("Too many trials found. Number of trials is greater than 20.")
        return 'too_many'

    elif num_trials == 0:
        logger.info("No trials found. Number of trials is 0.")
        print("No trials found. Number of trials is 0.")
        # Call increase_radius.py to increase the radius by 50 miles
        try:
            result = subprocess.run(['python', 'API_actions/increase_radius.py', STATE_FILE_PATH], check=True, capture_output=True, text=True)
            logger.info("Radius increased successfully.")
            print(result.stdout)
            if result.stderr:
                print(f"stderr: {result.stderr}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to increase radius: {e}")
            print(f"Failed to increase radius: {e}")
            print(f"stderr: {e.stderr}")
        return 'none_found'

    elif 1 <= num_trials <= 5:
        logger.info("Few trials found. Number of trials is between 1 and 5. Detailed output.")
        print("Few trials found. Detailed output.")
        display_main("detailed", json_path)
        return 'detailed_output'

    elif 6 <= num_trials <= 20:
        logger.info("A moderate number of trials found. Number of trials is between 6 and 20. Condensed output.")
        print("A moderate number of trials found. Condensed output.")
        display_main("condensed", json_path)
        return 'condensed_output'

    else:
        logger.error(f"No sort worked. The number of trials does not make sense. Number of trials: {num_trials}")
        print("No sort worked. The number of trials does not make sense.")
        return 'error'

if __name__ == "__main__":
    logger.info("Starting output_sort.py")

    if len(sys.argv) != 2:
        logger.error("Usage: python output_sort.py <stats_file>")
        print("Usage: python output_sort.py <stats_file>")
        sys.exit(1)

    stats_file = sys.argv[1]
    logger.debug(f"Stats file provided: {stats_file}")

    if not os.path.exists(stats_file):
        logger.error(f"Error: The stats file '{stats_file}' does not exist.")
        print(f"Error: The stats file '{stats_file}' does not exist.")
        sys.exit(1)

    try:
        logger.info(f"Opening stats file: {stats_file}")
        with open(stats_file, 'r') as file:
            stats = json.load(file)
            logger.debug(f"Stats content: {stats}")

        num_trials = stats.get('number_of_trials', 0)
        logger.info(f"Sorting and processing {num_trials} trials")
        result_type = sort_and_process_trials(num_trials)
        logger.debug(f"Result type: {result_type}")

    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
        print(f"JSON decoding error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

    logger.info("Completed output_sort.py")

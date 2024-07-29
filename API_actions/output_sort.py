# ./API_actions/output_sort.py

import logging
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from display_in_terminal.main import main as display_main

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

display_types = ["condensed", "detailed", "questions"]
json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../API_response/output_final_big.json'))

def sort_and_process_trials(num_trials):
    # Log the number of trials found
    logging.info(f"Number of trials found: {num_trials}")
    print(f"Number of trials found: {num_trials}")

    if num_trials > 20:
        logging.info("Too many trials found. Number of trials is greater than 20.")
        print("Too many trials found. Number of trials is greater than 20.")
        return 'too_many'

    elif num_trials == 0:
        logging.info("No trials found. Number of trials is 0.")
        print("No trials found. Number of trials is 0.")
        return 'none_found'

    elif 1 <= num_trials <= 5:
        logging.info("Few trials found. Number of trials is between 1 and 5. Detailed output.")
        print("Few trials found. Detailed output.")
        display_main("detailed", json_path)
        return 'detailed_output'

    elif 6 <= num_trials <= 20:
        logging.info("A moderate number of trials found. Number of trials is between 6 and 20. Condensed output.")
        print("A moderate number of trials found. Number of trials is between 6 and 20. Condensed output.")
        display_main("condensed", json_path)
        return 'condensed_output'

    else:
        logging.error(f"No sort worked. The number of trials does not make sense. Number of trials: {num_trials}")
        print("No sort worked. The number of trials does not make sense.")
        return 'error'

if __name__ == "__main__":
    logging.info("Starting output_sort.py")

    if len(sys.argv) != 2:
        logging.error("Usage: python output_sort.py <stats_file>")
        print("Usage: python output_sort.py <stats_file>")
        sys.exit(1)

    stats_file = sys.argv[1]
    logging.debug(f"Stats file provided: {stats_file}")

    if not os.path.exists(stats_file):
        logging.error(f"Error: The stats file '{stats_file}' does not exist.")
        print(f"Error: The stats file '{stats_file}' does not exist.")
        sys.exit(1)

    try:
        logging.info(f"Opening stats file: {stats_file}")
        with open(stats_file, 'r') as file:
            stats = json.load(file)
            logging.debug(f"Stats content: {stats}")

        num_trials = stats.get('number_of_trials', 0)
        logging.info(f"Sorting and processing {num_trials} trials")
        result_type = sort_and_process_trials(num_trials)
        logging.debug(f"Result type: {result_type}")

    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding error: {e}")
        print(f"JSON decoding error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

    logging.info("Completed output_sort.py")

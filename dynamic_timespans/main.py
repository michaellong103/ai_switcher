# ./dynamic_timespans/main.py

import os
import sys
import json
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from load_data import load_data
from sort_data import sort_by_days_until_end
from divide_groups import divide_into_groups
from calculate_data import calculate_group_data
from generate_answers_json import read_output_data as read_output_data_json, generate_answers_json, write_answers_to_file as write_answers_to_file_json
from generate_answers import read_output_data as read_output_data_txt, generate_answers, write_answers_to_file as write_answers_to_file_txt
from update_search_crit import main as update_search_crit_main

logging.basicConfig(level=logging.INFO)

def main():
    # Define the path to the input data
    input_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'API_response', 'dynamic_questions_input.json'))
    if not os.path.exists(input_data_path):
        logging.error(f"File not found: {input_data_path}")
        return

    # Load the data
    input_data = load_data(input_data_path)
    if not input_data or not isinstance(input_data, list):
        logging.error("Failed to load data or the data format is incorrect.")
        return

    # Sort and process the data
    sorted_trials = sort_by_days_until_end(input_data)
    logging.info(f"Sorted {len(sorted_trials)} trials by days until end.")

    groups = divide_into_groups(sorted_trials)
    logging.info(f"Divided trials into {len(groups)} groups.")

    calculated_data = calculate_group_data(groups)
    logging.info(f"Calculated additional data for {len(calculated_data)} groups.")

    # Write the results to both output_data.json and times_question_output.json
    output_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output_data.json'))
    times_question_output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'API_response', 'times_question_output.json'))

    with open(output_data_path, "w") as file:
        json.dump(calculated_data, file, indent=2)
        logging.info(f"Results written to {output_data_path}")

    with open(times_question_output_path, "w") as file:
        json.dump(calculated_data, file, indent=2)
        logging.info(f"Results also written to {times_question_output_path}")

    # Generate JSON answers
    try:
        output_data = read_output_data_json(output_data_path)
        answers_json = generate_answers_json(output_data)
        write_answers_to_file_json(answers_json, os.path.abspath(os.path.join(os.path.dirname(__file__), 'dynamic_timespans.json')))
        logging.info("generate_answers_json.py executed successfully.")
    except Exception as e:
        logging.error(f"Error occurred while running generate_answers_json.py: {e}")

    # Generate text answers
    try:
        output_data = read_output_data_txt(output_data_path)
        answers = generate_answers(output_data)
        write_answers_to_file_txt(answers, os.path.abspath(os.path.join(os.path.dirname(__file__), 'answers.txt')))
        logging.info("generate_answers.py executed successfully.")
    except Exception as e:
        logging.error(f"Error occurred while running generate_answers.py: {e}")

    # Update SearchCrit.json
    try:
        update_search_crit_main()
        logging.info("update_search_crit.py executed successfully.")
    except Exception as e:
        logging.error(f"Error occurred while running update_search_crit.py: {e}")

if __name__ == "__main__":
    main()

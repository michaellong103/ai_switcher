# ./dynamic_timespans/update_search_crit.py

import json
import os
import sys
import logging  # New import

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def load_json_file(filepath):
    logging.info(f"Loading JSON file from: {filepath}")
    with open(filepath, 'r') as file:
        data = json.load(file)
    logging.info(f"Loaded data: {json.dumps(data, indent=2)}")
    return data

def save_json_file(filepath, data):
    logging.info(f"Saving JSON file to: {filepath}")
    logging.info(f"Data being saved: {json.dumps(data, indent=2)}")
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=2)

def main():
    # Define the paths to the JSON files
    dynamic_timespans_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'dynamic_timespans.json'))
    search_question_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'API_response', 'SearchQuestion.json'))

    logging.info(f"Dynamic timespans path: {dynamic_timespans_path}")
    logging.info(f"Search question path: {search_question_path}")

    # Load the dynamic_timespans.json content
    if not os.path.exists(dynamic_timespans_path):
        logging.error(f"File not found: {dynamic_timespans_path}")
        return
    dynamic_timespans_data = load_json_file(dynamic_timespans_path)

    # Prepare the data to be saved in SearchQuestion.json
    search_question_data = {
        "question_categories": [dynamic_timespans_data]
    }
    logging.info(f"Prepared search question data: {json.dumps(search_question_data, indent=2)}")

    # Save the new data to SearchQuestion.json
    save_json_file(search_question_path, search_question_data)
    logging.info(f"Saved updated question categories to {search_question_path}")

if __name__ == "__main__":
    main()

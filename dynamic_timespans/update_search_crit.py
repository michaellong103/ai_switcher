# ./dynamic_timespans/update_search_crit.py

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def load_json_file(filepath):
    print(f"Loading JSON file from: {filepath}")  # Debugging statement
    with open(filepath, 'r') as file:
        data = json.load(file)
    print(f"Loaded data: {json.dumps(data, indent=2)}")  # Debugging statement
    return data

def save_json_file(filepath, data):
    print(f"Saving JSON file to: {filepath}")  # Debugging statement
    print(f"Data being saved: {json.dumps(data, indent=2)}")  # Debugging statement
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=2)

def main():
    # Define the paths to the JSON files
    dynamic_timespans_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'dynamic_timespans.json'))
    search_question_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'API_response', 'SearchQuestion.json'))

    print(f"Dynamic timespans path: {dynamic_timespans_path}")  # Debugging statement
    print(f"Search question path: {search_question_path}")  # Debugging statement

    # Load the dynamic_timespans.json content
    if not os.path.exists(dynamic_timespans_path):
        print(f"File not found: {dynamic_timespans_path}")
        return
    dynamic_timespans_data = load_json_file(dynamic_timespans_path)

    # Prepare the data to be saved in SearchQuestion.json
    search_question_data = {
        "question_categories": [dynamic_timespans_data]
    }
    print(f"Prepared search question data: {json.dumps(search_question_data, indent=2)}")  # Debugging statement

    # Save the new data to SearchQuestion.json
    save_json_file(search_question_path, search_question_data)
    print(f"Saved updated question categories to {search_question_path}")

if __name__ == "__main__":
    main()

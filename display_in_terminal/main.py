# display_in_terminal/main.py

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from interfaces.interface_generator import condensed_trials, detailed_trials, question_format

def find_output_directory():
    possible_paths = [
        'API_response', '/API_response', '../API_response', '../../API_response',
        'API_response/', '/API_response/', '../API_response/', '../../API_response/'
    ]
    
    for path in possible_paths:
        abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))
        if os.path.exists(abs_path):
            return abs_path
    
    # If none of the paths exist, create the first one
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), possible_paths[0]))
    os.makedirs(abs_path)
    return abs_path

def main(display_type, json_path):
    with open(json_path, 'r') as file:
        trials_json = file.read()
    
    trials = json.loads(trials_json)

    if display_type == "condensed":
        output = condensed_trials(trials)
    elif display_type == "detailed":
        output = detailed_trials(trials)
    elif display_type == "questions":
        output = question_format(trials)

    output_dir = find_output_directory()

    output_file_path = os.path.join(output_dir, f"{display_type}_output.txt")
    with open(output_file_path, 'w') as output_file:
        output_file.write(output)

    print(f"Output saved to {output_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate formatted trial information from a JSON file.")
    parser.add_argument("display_type", choices=["condensed", "detailed", "questions"], help="Type of display format")
    parser.add_argument("json_path", help="Path to the JSON file containing trial information")

    args = parser.parse_args()

    main(args.display_type, args.json_path)

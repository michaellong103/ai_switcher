# ./display_in_terminal/main.py

import argparse
import json
import os
import sys

# Add the parent directory and the display_in_terminal directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from interfaces.interface_generator import condensed_trials, detailed_trials, question_format

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

    print(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate formatted trial information from a JSON file.")
    parser.add_argument("display_type", choices=["condensed", "detailed", "questions"], help="Type of display format")
    parser.add_argument("json_path", help="Path to the JSON file containing trial information")

    args = parser.parse_args()

    main(args.display_type, args.json_path)

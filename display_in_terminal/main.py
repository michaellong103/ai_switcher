# ./main.py

import argparse
import json
import logging
from interfaces.interface_generator import condensed_trials, detailed_trials, question_format

def main():
    parser = argparse.ArgumentParser(description="Generate formatted trial information from a JSON file.")
    parser.add_argument("display_type", choices=["condensed", "detailed", "questions"], help="Type of display format")
    parser.add_argument("json_path", help="Path to the JSON file containing trial information")

    args = parser.parse_args()

    with open(args.json_path, 'r') as file:
        trials_json = file.read()
    
    trials = json.loads(trials_json)

    if args.display_type == "condensed":
        output = condensed_trials(trials)
    elif args.display_type == "detailed":
        output = detailed_trials(trials)
    elif args.display_type == "questions":
        output = question_format(trials)

    print(output)

if __name__ == "__main__":
    main()

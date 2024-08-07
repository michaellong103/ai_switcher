# ./main.py

import argparse
import json
import os
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from interfaces.interface_generator import condensed_trials, detailed_trials, question_format

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def find_output_directory():
    """
    Finds or creates the output directory for storing result files.

    Returns:
        str: The path to the output directory.
    """
    possible_paths = [
        '../API_response'
    ]
    
    for path in possible_paths:
        abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), path))
        logging.debug(f"Checking directory: {abs_path}")
        if os.path.exists(abs_path):
            logging.info(f"Using existing directory: {abs_path}")
            return abs_path
    
    # If none of the paths exist, create the first one
    abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), possible_paths[0]))
    logging.info(f"None of the paths exist. Creating directory: {abs_path}")
    os.makedirs(abs_path)
    return abs_path

def run_main(display_type, json_path):
    """
    Main function to process trials and generate output.

    Args:
        display_type (str): Type of display format (condensed, detailed, or questions).
        json_path (str): Path to the JSON file containing trial information.
    """
    logging.info(f"Starting run_main with display_type={display_type} and json_path={json_path}")
    
    try:
        with open(json_path, 'r') as file:
            trials_json = file.read()
            logging.debug(f"Read JSON data from {json_path}")
    except FileNotFoundError as e:
        logging.error(f"File not found: {json_path}. Error: {e}")
        return
    except Exception as e:
        logging.error(f"Error reading file {json_path}: {e}")
        return
    
    try:
        trials = json.loads(trials_json)
        logging.info(f"Loaded {len(trials)} trials from JSON")
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON: {e}")
        return

    # Generate output based on display type
    if display_type == "condensed":
        output = condensed_trials(trials)
    elif display_type == "detailed":
        output = detailed_trials(trials)
    elif display_type == "questions":
        output = question_format(trials)
    else:
        logging.warning(f"Unknown display_type: {display_type}")
        return

    output_dir = find_output_directory()

    # Create and save the output file
    output_file_path = os.path.join(output_dir, f"{display_type}_output.txt")
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write(output)
            logging.info(f"Output saved to {output_file_path}")
    except Exception as e:
        logging.error(f"Failed to write output to {output_file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate formatted trial information from a JSON file.")
    parser.add_argument("display_type", choices=["condensed", "detailed", "questions"], help="Type of display format")
    parser.add_argument("json_path", help="Path to the JSON file containing trial information")

    args = parser.parse_args()

    run_main(args.display_type, args.json_path)

if __name__ == "__main__":
    main()

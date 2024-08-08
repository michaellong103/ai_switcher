# ./main.py

import argparse
import json
import os
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from interfaces.interface_generator import condensed_trials, detailed_trials, question_format

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


def run_main(mode):
    """
    Main function to display data in terminal based on the mode.

    Args:
        mode (str): Mode to display data, either 'detailed', 'condensed', or 'questions'.
    """
    logging.info(f"run_main called with mode: {mode}")

    # Determine the base directory of the script
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    # Determine the path based on the mode
    if mode == 'detailed':
        file_path = os.path.join(base_dir, '../API_response/detailed.json')
    elif mode == 'condensed':
        file_path = os.path.join(base_dir, '../API_response/condensed.json')
    elif mode == 'questions':
        file_path = os.path.join(base_dir, '../API_response/questions.json')
    else:
        logging.error(f"Invalid mode: {mode}")
        return

    # Check if the file exists
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            logging.info(f"Loaded data from {file_path}")

            # Format data based on the mode
            if mode == 'detailed':
                output = detailed_trials(data)
            elif mode == 'condensed':
                output = condensed_trials(data)
            elif mode == 'questions':
                output = question_format(data)

            # Display the formatted output
            print(output)
            
    except FileNotFoundError as e:
        logging.error(f"File not found: {file_path}. Error: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON from file: {file_path}. Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Generate formatted trial information from a JSON file.")
    parser.add_argument("display_type", choices=["condensed", "detailed", "questions", "both"], help="Type of display format")

    args = parser.parse_args()

    logging.debug(f"Parsed arguments: {args}")
    logging.info(f"Calling run_main with display_type={args.display_type}")

    run_main(args.display_type)


if __name__ == "__main__":
    main()

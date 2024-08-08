# ./display_json/display_json.py

import os
import json
from display_json.palette import CYAN, YELLOW, RESET_COLOR

def banner(text):
    return f"{CYAN}{'=' * 40}\n{text}\n{'=' * 40}{RESET_COLOR}"

def condensed_trials(trials):
    output = f"{banner(f'Condensed Trials: ({len(trials)} trials)')}\n\n"
    for trial in trials:
        title = trial['briefTitle']
        nct_id = trial['nctNumber']
        output += f"{CYAN}{title}{RESET_COLOR}\n{YELLOW}{nct_id}{RESET_COLOR}\n\n"
    return output

def detailed_trials(trials):
    output = f"{banner(f'Detailed Trials: ({len(trials)} trials)')}\n\n"
    for trial in trials:
        title = trial['briefTitle']
        description = trial['briefSummary']
        nct_id = trial['nctNumber']
        output += f"{CYAN}{title}{RESET_COLOR}\n{description}\n{YELLOW}{nct_id}{RESET_COLOR}\n\n"
    return output

def load_and_display_json():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    condensed_file_path = os.path.join(script_dir, "..", "API_response", "condensed.json")
    detailed_file_path = os.path.join(script_dir, "..", "API_response", "detailed.json")

    # Load and display condensed.json
    try:
        with open(condensed_file_path, 'r') as file:
            condensed_data = json.load(file)
        print("Contents of condensed.json:")
        print(condensed_trials(condensed_data))
    except FileNotFoundError:
        print("Failed to load condensed.json")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from condensed.json: {e}")

    # Load and display detailed.json
    try:
        with open(detailed_file_path, 'r') as file:
            detailed_data = json.load(file)
        print("\nContents of detailed.json:")
        print(detailed_trials(detailed_data))
    except FileNotFoundError:
        print("Failed to load detailed.json")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from detailed.json: {e}")

if __name__ == "__main__":
    load_and_display_json()

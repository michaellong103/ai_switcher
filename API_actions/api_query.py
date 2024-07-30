# ./API_actions/api_query.py
import sys
import os
import json
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from api_client import query_clinical_trials, query_clinical_trial_by_nct
from api_json_handler import read_json, write_json
from async_tasks import async_main

STATE_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'config_state.json')

def update_state_with_input(input_file):
    try:
        # Read input file content
        input_data = read_json(input_file)

        # Load current state
        if os.path.exists(STATE_FILE_PATH):
            with open(STATE_FILE_PATH, 'r') as state_file:
                state_data = json.load(state_file)
        else:
            state_data = {}

        # Update the state with the current API call
        state_data["current_api_params"] = input_data

        # Save the updated state back to the state file
        with open(STATE_FILE_PATH, 'w') as state_file:
            json.dump(state_data, state_file, indent=4)

        print(f"State updated with current API call from {input_file}")

    except Exception as e:
        print(f"Failed to update state with input file content: {e}")

def main(input_file, output_file):
    # Update the state with the input file content
    update_state_with_input(input_file)

    # Execute the main asynchronous task
    api_response = asyncio.run(async_main(input_file, output_file))
    if api_response is not None:
        print(json.dumps(api_response, indent=4))
    return api_response

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python api_query.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)

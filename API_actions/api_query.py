# ./API_actions/api_query.py

import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from api_client import query_clinical_trials, query_clinical_trial_by_nct
from api_json_handler import read_json, write_json

def main(input_file, output_file):
    # Read input JSON
    input_data = read_json(input_file)
    
    if 'nct_number' in input_data:
        # Query a single clinical trial based on NCT number
        api_response = query_clinical_trial_by_nct(input_data['nct_number'])
    else:
        # Query multiple clinical trials
        api_response = query_clinical_trials(input_data)

    # Write the API response to output JSON
    write_json(api_response, output_file)

if __name__ == "__main__":
    input_file = 'input.json'
    output_file = 'output.json'
    main(input_file, output_file)

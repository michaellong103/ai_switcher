# ./API_query/clinical_trials_query.py

import os
import json
import requests
import argparse
import logging
import sys

def load_input(file_path):
    """
    Load input data from a JSON file.
    
    :param file_path: Path to the input JSON file
    :return: Data extracted from the JSON file as a dictionary
    """
    with open(file_path, 'r') as f:
        return json.load(f)

def construct_query_url(data, radius=100):
    """
    Construct a query URL for the clinical trials API.

    :param data: Dictionary containing input parameters
    :param radius: Radius for the location search in kilometers
    :return: Constructed query URL as a string
    """
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "format": "json",
        "query.cond": data["Medical Condition"].replace(" ", "+"),
        "pageSize": 200,
        "filter.overallStatus": "RECRUITING|NOT_YET_RECRUITING|AVAILABLE",
        "filter.geo": f"distance({data['Latitude']},{data['Longitude']},{radius})"
    }
    
    query_url = f"{base_url}?{'&'.join(f'{key}={value}' for key, value in params.items())}"
    return query_url

def fetch_clinical_trials(query_url):
    """
    Fetch clinical trials data from the given URL.

    :param query_url: URL to fetch data from
    :return: JSON response from the API as a dictionary
    """
    try:
        response = requests.get(query_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    return None

def save_output(data, file_path):
    """
    Save data to an output JSON file.

    :param data: Data to be saved
    :param file_path: Path to the output JSON file
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def main(input_file_path, output_file_path):
    # Load input data
    input_data = load_input(input_file_path)

    # Construct query URL
    query_url = construct_query_url(input_data, radius=150) # Using 150 km as an example

    # Fetch data
    clinical_trials_data = fetch_clinical_trials(query_url)

    if clinical_trials_data:
        # Save data to output
        save_output(clinical_trials_data, output_file_path)
        print(f"Results saved to {output_file_path}")
    else:
        print("Failed to fetch clinical trials data.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clinical Trials Query')
    parser.add_argument('input_file', type=str, help='Path to the input JSON file')
    parser.add_argument('output_file', type=str, help='Path to the output JSON file')
    
    args = parser.parse_args()
    main(args.input_file, args.output_file)

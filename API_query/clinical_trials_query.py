# ./clinical_trials_query.py

import os
import json
import requests
import sys
import logging

try:
    # Attempt relative import for when running within a package
    from .query_logger import log_query
    from .update_config_state import update_config_state  # Import update_config_state
    from .update_stats import update_stats  # Import update_stats
except ImportError:
    # Fall back to absolute import if relative import fails
    from query_logger import log_query
    from update_config_state import update_config_state  # Import update_config_state
    from update_stats import update_stats  # Import update_stats

# Configure logging to output to both a file and standard output
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture detailed logs
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s',
    handlers=[
        logging.FileHandler("clinical_trials_query.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def load_input(file_path):
    """
    Load input data from a JSON file.

    :param file_path: Path to the input JSON file
    :return: Data extracted from the JSON file as a dictionary
    """
    if not os.path.exists(file_path):
        logging.error(f"Input file not found: {file_path}")
        raise FileNotFoundError(f"Input file not found: {file_path}")

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            logging.info(f"Input data loaded from {file_path}")
            return data
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        raise

def construct_query_url(data, default_radius=10):
    """
    Construct a query URL for the clinical trials API.

    :param data: Dictionary containing input parameters
    :param default_radius: Default radius for the location search in kilometers
    :return: Constructed query URL as a string
    """
    # Determine the radius to use: from input data or default
    radius = data.get("Radius", default_radius)

    # Base URL for the API
    base_url = "https://clinicaltrials.gov/api/v2/studies"

    # Parameters for the API query
    params = {
        "format": "json",
        "query.cond": data["Medical Condition"].replace(" ", "+"),
        "pageSize": 200,
        "filter.overallStatus": "RECRUITING|NOT_YET_RECRUITING|AVAILABLE",
        "filter.geo": f"distance({data['Latitude']},{data['Longitude']},{radius})"
    }

    # Constructing the query URL
    query_url = f"{base_url}?{'&'.join(f'{key}={value}' for key, value in params.items())}"

    # Log the query using the newly created logging module
    log_query(query_url, data)
    logging.info(f"Constructed query URL: {query_url}")

    return query_url

def fetch_clinical_trials(query_url):
    """
    Fetch clinical trials data from the given URL.

    :param query_url: URL to fetch data from
    :return: JSON response from the API as a dictionary
    """
    try:
        logging.info(f"Fetching data from API: {query_url}")
        response = requests.get(query_url, timeout=10)
        response.raise_for_status()
        logging.info("Data fetched successfully from the API.")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"An error occurred: {req_err}")

    return None

def extract_nct_ids(response_data):
    """
    Extract NCT IDs from the API response data.

    :param response_data: The JSON response data from the API
    :return: List of NCT IDs found in the response
    """
    nct_ids = []

    # Traverse the response to extract NCT IDs
    if "studies" in response_data:
        for study in response_data["studies"]:
            if "nctId" in study:
                nct_ids.append(study["nctId"])

    if nct_ids:
        logging.info(f"Extracted NCT IDs: {', '.join(nct_ids)}")
    else:
        logging.warning("Query returned no studies or no NCT IDs found.")

    return nct_ids

def save_output(data, file_path):
    """
    Save data to an output JSON file.

    :param data: Data to be saved
    :param file_path: Path to the output JSON file
    """
    try:
        # Only create directories if the path includes a directory
        dir_name = os.path.dirname(file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        logging.info(f"Data successfully saved to {file_path}")
    except IOError as e:
        logging.error(f"Failed to write output data to {file_path}: {e}")
        raise

def check_file_path(file_path):
    """
    Check if the given file path exists and log the result.

    :param file_path: Path to the file to check
    """
    if os.path.exists(file_path):
        logging.info(f"The file '{file_path}' exists.")
    else:
        logging.error(f"The file '{file_path}' does not exist.")

def main():
    logging.info("Starting Clinical Trials Query Process")
    
    # Hard-coded paths for the input and output JSON files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, "input.json")
    output_file_path_1 = os.path.join(script_dir, "output.json")
    output_file_path_2 = os.path.join(script_dir, "..", "API_response", "finaloutput.json")

    # Log file paths
    logging.debug("Checking file paths...")
    
    # Check each file path
    logging.debug("Checking input file path...")
    check_file_path(input_file_path)

    logging.debug("Checking output file path 1...")
    check_file_path(output_file_path_1)

    logging.debug("Checking output file path 2...")
    check_file_path(output_file_path_2)
    
    # Load input data
    try:
        input_data = load_input(input_file_path)
        logging.info("Input data loaded successfully.")
    except FileNotFoundError as e:
        logging.error(e)
        sys.exit(1)
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        sys.exit(1)

    # Construct query URL, use default radius if "Radius" is not in the input data
    query_url = construct_query_url(input_data)

    # Update the config state file with current API parameters and query URL
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_dir, "..",  "config_state.json")
    
    update_config_state(input_data, config_file_path)
    update_stats(input_data, config_file_path)

    # Fetch data
    clinical_trials_data = fetch_clinical_trials(query_url)

    if clinical_trials_data:
        # Extract NCT IDs
        nct_ids = extract_nct_ids(clinical_trials_data)

        # Save data to output files
        save_output(clinical_trials_data, output_file_path_1)
        save_output(clinical_trials_data, output_file_path_2)
        logging.info(f"Results saved to {output_file_path_1} and {output_file_path_2}")
    else:
        logging.error("Failed to fetch clinical trials data.")

if __name__ == "__main__":
    logging.debug("Starting main function.")
    main()
    logging.debug("Finished executing main function.")

# ./info_extraction.py

import os
import logging

try:
    from .file_utils import save_json_to_file
except ImportError:
    from file_utils import save_json_to_file

def extract_condensed_info(trial_data, output_dir):
    """
    Extracts condensed information from trial data.

    Args:
        trial_data (list): List of trial data dictionaries.
        output_dir (str): Directory to save condensed data.

    Returns:
        list: A list of condensed clinical trial information.
    """
    condensed_data = []

    for trial in trial_data:
        identification_module = trial.get("protocolSection", {}).get("identificationModule", {})
        nct_id = identification_module.get("nctId", "Unknown")
        brief_title = identification_module.get("briefTitle", "No Title")

        logging.debug(f"Condensing trial with NCT ID: {nct_id}")

        condensed_info = {
            "nctNumber": nct_id,
            "briefTitle": brief_title
        }

        condensed_data.append(condensed_info)

    # Save the condensed data
    condensed_file_path = os.path.join(output_dir, 'condensed.json')
    save_json_to_file(condensed_data, condensed_file_path, "Condensed data with brief titles")

    return condensed_data


def extract_detailed_info(trial_data, output_dir):
    """
    Extracts detailed information from trial data.

    Args:
        trial_data (list): List of trial data dictionaries.
        output_dir (str): Directory to save detailed data.

    Returns:
        list: A list of detailed clinical trial information.
    """
    detailed_data = []

    for trial in trial_data:
        protocol_section = trial.get("protocolSection", {})
        identification_module = protocol_section.get("identificationModule", {})
        description_module = protocol_section.get("descriptionModule", {})
        
        nct_id = identification_module.get("nctId", "Unknown")
        brief_title = identification_module.get("briefTitle", "No Title")
        brief_summary = description_module.get("briefSummary", "No Summary")

        logging.debug(f"Detailing trial with NCT ID: {nct_id}")

        detailed_info = {
            "nctNumber": nct_id,
            "briefTitle": brief_title,
            "briefSummary": brief_summary
        }

        detailed_data.append(detailed_info)

    # Save the detailed data
    detailed_file_path = os.path.join(output_dir, 'detailed.json')
    save_json_to_file(detailed_data, detailed_file_path, "Detailed data with brief titles and summaries")

    return detailed_data


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 3:
        logging.error("Usage: python info_extraction.py <input_json_file> <output_dir>")
        sys.exit(1)

    # Dynamic path construction
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_json_file = os.path.join(script_dir, sys.argv[1])
    output_dir = os.path.join(script_dir, sys.argv[2])

    try:
        with open(input_json_file, 'r') as file:
            trials_data = json.load(file)['studies']
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load JSON data: {e}")
        sys.exit(1)

    # Extract both condensed and detailed info
    extract_condensed_info(trials_data, output_dir)
    extract_detailed_info(trials_data, output_dir)

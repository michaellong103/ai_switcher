# ./utils.py

import json
import numpy as np
import logging

def load_json(file_path):
    """Load JSON data from a file."""
    logging.info(f"Loading JSON data from {file_path}")
    with open(file_path, 'r') as file:
        data = json.load(file)
    logging.info(f"Successfully loaded JSON data: {file_path}")
    return data

def find_best_group_in_times_json(times_data):
    """Find the largest group in times_question_output.json that is closest to but does not exceed 10 trials."""
    logging.info("Starting search for best group in times_question_output.json")
    
    best_group = None
    closest_count = 0
    trial_counts = []
    num_groups = 0

    if isinstance(times_data, list):
        for index, group in enumerate(times_data):
            trial_count = group.get('total', 0)
            group_name = group.get('trialGroup', f"Group {index + 1}")
            trial_counts.append(trial_count)
            num_groups += 1

            logging.info(f"[Group {index + 1}] '{group_name}' has {trial_count} trials.")
            logging.info(f"Checking if '{group_name}' with {trial_count} trials is the best group so far...")

            if 0 < trial_count <= 10 and trial_count > closest_count:
                logging.info(f"'{group_name}' is now the best group found so far with {trial_count} trials.")
                closest_count = trial_count
                best_group = group

    if best_group:
        logging.info(f"Final best group found: '{best_group.get('trialGroup', 'Unnamed')}' with {closest_count} trials.")
    else:
        logging.warning("No valid group found in times_question_output.json.")

    logging.info(f"Total number of groups in 'times_question_output.json': {num_groups}")
    return best_group, closest_count, trial_counts

def find_best_group_in_phase_json(phase_data):
    """Find the largest group in phase_question_output.json that is closest to but does not exceed 10 trials."""
    logging.info("Starting search for best option in phase_question_output.json")

    best_group = None
    closest_count = 0
    trial_counts = []
    num_groups = 0

    if 'options' in phase_data:
        for index, option in enumerate(phase_data['options']):
            trial_count = option.get('NCTCount', 0)
            option_name = option.get('optionText', f"Option {index + 1}")
            trial_counts.append(trial_count)
            num_groups += 1

            logging.info(f"[Option {index + 1}] '{option_name}' has {trial_count} trials.")
            logging.info(f"Checking if '{option_name}' with {trial_count} trials is the best option so far...")

            if 0 < trial_count <= 10 and trial_count > closest_count:
                logging.info(f"'{option_name}' is now the best option found so far with {trial_count} trials.")
                closest_count = trial_count
                best_group = option

    if best_group:
        logging.info(f"Final best option found: '{best_group.get('optionText', 'Unnamed')}' with {closest_count} trials.")
    else:
        logging.warning("No valid option found in phase_question_output.json.")

    logging.info(f"Total number of options in 'phase_question_output.json': {num_groups}")
    return best_group, closest_count, trial_counts

def calculate_mad(trial_counts):
    """Calculate the Mean Absolute Deviation (MAD) for a list of trial counts."""
    logging.info("Calculating MAD and mean for trial counts")
    if len(trial_counts) == 0:
        logging.warning("No trial counts provided, returning None for MAD and mean.")
        return None, None
    mean = np.mean(trial_counts)
    deviations = [abs(x - mean) for x in trial_counts]
    mad = np.mean(deviations)
    logging.info(f"Calculated MAD: {mad}, Mean: {mean}")
    return mad, mean

def print_group_info(group, group_name, source_file, count):
    """Log the group name, source file, and count."""
    logging.info(f"Group: {group_name} from {source_file} with {count} trials")

def extract_nct_numbers_from_times(times_data):
    """Extract all NCT numbers from times_question_output.json."""
    logging.info("Extracting NCT numbers from times_question_output.json")
    return {nct for group in times_data for nct_dict in group['nctNumbers'] for nct in nct_dict}

def extract_nct_numbers_from_phase(phase_data):
    """Extract all NCT numbers from phase_question_output.json."""
    logging.info("Extracting NCT numbers from phase_question_output.json")
    return {nct for option in phase_data.get('options', []) for nct in option['NCTNumbers']}

def find_duplicated_trials(times_ncts, phase_ncts):
    """Find duplicated NCT numbers between times and phase data."""
    logging.info("Finding duplicated NCT numbers between times and phase data")
    duplicates = list(times_ncts.intersection(phase_ncts))
    logging.info(f"Found {len(duplicates)} duplicated NCT numbers.")
    return duplicates, len(duplicates)

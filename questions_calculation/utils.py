# ./utils.py
import json
import numpy as np
import logging

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def find_best_group_in_times_json(times_data):
    """Find the largest group in times_question_output.json that is closest to but does not exceed 10 trials."""
    best_group = None
    closest_count = 0
    trial_counts = []
    num_groups = 0

    if isinstance(times_data, list):
        for group in times_data:
            trial_count = group['total']
            trial_counts.append(trial_count)
            num_groups += 1
            logging.info(f"Group '{group['trialGroup']}' has {trial_count} trials.")
            if 0 < trial_count <= 10 and trial_count > closest_count:
                closest_count = trial_count
                best_group = group

    logging.info(f"Total number of groups in 'times_question_output.json': {num_groups}")
    return best_group, closest_count, trial_counts

def find_best_group_in_phase_json(phase_data):
    """Find the largest group in phase_question_output.json that is closest to but does not exceed 10 trials."""
    best_group = None
    closest_count = 0
    trial_counts = []
    num_groups = 0

    if 'options' in phase_data:
        for option in phase_data['options']:
            trial_counts.append(option['NCTCount'])
            num_groups += 1
            logging.info(f"Group '{option['optionText']}' has {option['NCTCount']} trials.")
            if 0 < option['NCTCount'] <= 10 and option['NCTCount'] > closest_count:
                closest_count = option['NCTCount']
                best_group = option

    logging.info(f"Total number of groups in 'phase_question_output.json': {num_groups}")
    return best_group, closest_count, trial_counts

def calculate_mad(trial_counts):
    """Calculate the Mean Absolute Deviation (MAD) for a list of trial counts."""
    if len(trial_counts) == 0:
        return None, None
    mean = np.mean(trial_counts)
    deviations = [abs(x - mean) for x in trial_counts]
    mad = np.mean(deviations)
    return mad, mean

def print_group_info(group, group_name, source_file, count):
    """Log the group name, source file, and count."""
    logging.info(f"Group: {group_name} from {source_file} with {count} trials")

def extract_nct_numbers_from_times(times_data):
    """Extract all NCT numbers from times_question_output.json."""
    return {nct for group in times_data for nct_dict in group['nctNumbers'] for nct in nct_dict}

def extract_nct_numbers_from_phase(phase_data):
    """Extract all NCT numbers from phase_question_output.json."""
    return {nct for option in phase_data.get('options', []) for nct in option['NCTNumbers']}

def find_duplicated_trials(times_ncts, phase_ncts):
    """Find duplicated NCT numbers between times and phase data."""
    duplicates = list(times_ncts.intersection(phase_ncts))
    return duplicates, len(duplicates)

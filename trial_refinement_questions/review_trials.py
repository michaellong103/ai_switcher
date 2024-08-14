# ./trial_refinement_questions/review_trials.py
import json
import os
import logging
from datetime import datetime

log_file_path = os.path.join(os.path.dirname(__file__), 'trial_analysis.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)  # Only show warnings and above in console

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def load_trial_data(file_path):
    """Load trial data from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        logger.error(f"The file '{file_path}' was not found.")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from '{file_path}': {e}")
        return None

def normalize_trials_data(trials_data):
    """Normalize the structure of trials_data to ensure it's a list of dictionaries."""
    if isinstance(trials_data, str):
        try:
            trials_data = json.loads(trials_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")

    if isinstance(trials_data, dict):
        if 'studies' in trials_data:
            trials_data = trials_data['studies']
        else:
            trials_data = [trials_data]  # Wrap a single trial in a list

    if not isinstance(trials_data, list) or not all(isinstance(item, dict) for item in trials_data):
        raise ValueError("Expected a list of dictionaries representing trials.")

    return trials_data

def load_api_params(config_file):
    """Load API parameters from a configuration file."""
    try:
        with open(config_file, 'r') as f:
            config_data = json.load(f)
            return config_data.get("current_api_params", {})
    except FileNotFoundError:
        logger.error(f"The configuration file '{config_file}' was not found.")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from '{config_file}': {e}")
        return None

def display_api_params(api_params):
    """Display API parameters to the user (only in the log file)."""
    logger.info("Too many trials were returned for the following API parameters:")
    for key, value in api_params.items():
        logger.info(f"  {key}: {value}")
    logger.info("")  # Add an extra line for readability

def analyze_data(trials_data):
    """Analyze data to suggest the best filtering option."""
    date_filter_count = len(set(trial['date'] for trial in trials_data if 'date' in trial))
    phase_filter_count = len(set(trial['phase'] for trial in trials_data if 'phase' in trial))
    
    if date_filter_count < phase_filter_count:
        logger.info(f"Based on the analysis, filtering by 'date' might be more effective.")
        return 'date'
    else:
        logger.info(f"Based on the analysis, filtering by 'phase' might be more effective.")
        return 'phase'

def ask_user_for_filtering_option(best_option):
    """Ask the user for the preferred filtering option."""
    logger.info(f"Suggesting filtering by '{best_option}'.")
    choice = input(f"Do you want to filter by '{best_option}' or the other option? (type 'date' or 'phase'): ")
    return choice.strip().lower()

def filter_by_phase(trials_data, phase):
    """Filter trials data by a specific phase."""
    if not phase:
        logger.warning("No phase specified for filtering.")
        return trials_data  # If no phase is provided, return the unfiltered data

    filtered_trials = []
    missing_phase_count = 0

    for trial in trials_data:
        trial_phase = trial.get('phase')
        
        if trial_phase is None:
            missing_phase_count += 1
            logger.warning(f"Trial missing 'phase' key: {trial}")
            continue
        
        if trial_phase.lower() == phase.lower():
            filtered_trials.append(trial)
    
    logger.info(f"Filtered {len(filtered_trials)} trials for phase '{phase}'.")
    if missing_phase_count > 0:
        logger.info(f"{missing_phase_count} trials were missing phase information and were excluded.")

    return filtered_trials

def filter_by_date(trials_data, start_date=None, end_date=None):
    """Filter trials data by a date range."""
    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            logger.error(f"Invalid start date format: {start_date}. Expected format is YYYY-MM-DD.")
            return []

    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            logger.error(f"Invalid end date format: {end_date}. Expected format is YYYY-MM-DD.")
            return []

    filtered_trials = []
    for trial in trials_data:
        try:
            trial_date = datetime.strptime(trial['date'], "%Y-%m-%d")
        except (KeyError, ValueError):
            logger.warning(f"Skipping trial due to invalid or missing date: {trial}")
            continue
        
        if start_date and trial_date < start_date:
            continue
        if end_date and trial_date > end_date:
            continue
        filtered_trials.append(trial)
    
    logger.info(f"Filtered {len(filtered_trials)} trials based on the provided date range.")
    return filtered_trials

def main():
    """Main function to load, analyze, and filter trial data."""
    # Navigate to the parent directory
    base_dir = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

    # Construct paths to the required files
    file_path = os.path.join(base_dir, 'API_response', 'finaloutput.json')
    config_file = os.path.join(base_dir, 'config_state.json')

    # Load the API parameters and display them to the user
    api_params = load_api_params(config_file)
    if not api_params:
        return  # Exit if the API parameters could not be loaded
    display_api_params(api_params)

    # Load the trial data
    trials_data = load_trial_data(file_path)
    if not trials_data:
        return  # Exit if the trial data could not be loaded

    # Normalize the trial data structure
    try:
        trials_data = normalize_trials_data(trials_data)
    except ValueError as e:
        logger.error(f"Error: {e}")
        return

    # Analyze the data to determine the best filtering option
    best_option = analyze_data(trials_data)

    # Ask the user for the filtering preference
    user_choice = ask_user_for_filtering_option(best_option)

    # Apply the selected filter
    if user_choice == 'date':
        start_date = input("Enter start date (YYYY-MM-DD) or press Enter to skip: ")
        end_date = input("Enter end date (YYYY-MM-DD) or press Enter to skip: ")
        filtered_data = filter_by_date(trials_data, start_date=start_date, end_date=end_date)
    elif user_choice == 'phase':
        phase = input("Enter trial phase (e.g., Phase I, Phase II): ")
        filtered_data = filter_by_phase(trials_data, phase=phase)
    else:
        logger.error("Invalid choice. No filtering applied.")
        return

    # Output the filtered data
    logger.info(f"Filtered data: {json.dumps(filtered_data, indent=2)}")

if __name__ == "__main__":
    main()

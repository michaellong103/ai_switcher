# ./trial_refinement_questions/main.py
import json
import os
from logging_config import logger
from date_utils import filter_by_date
from phase_utils import filter_by_phase, analyze_data, ask_user_for_filtering_option

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

def main():
    """Main function to load, analyze, and filter trial data."""
    # Navigate to the parent directory
    base_dir = os.path.abspath(os.path.join(__file__, os.pardir))

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

    # Output the filtered data (already logged in the filter function)

if __name__ == "__main__":
    main()

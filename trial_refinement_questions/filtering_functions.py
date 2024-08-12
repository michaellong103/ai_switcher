# ./trial_refinement_questions/filtering_functions.py

from datetime import datetime


def filter_by_phase(trials_data, phase):
    """
    Filter trials data by a specific phase, logging any trials that are missing phase information.
    
    Args:
        trials_data (list): A list of dictionaries where each dictionary represents a trial.
        phase (str): The phase to filter trials by (e.g., 'Phase I', 'Phase II').

    Returns:
        list: A list of filtered trials matching the specified phase.
    """
    if not phase:
        logging.warning("No phase specified for filtering.")
        return trials_data  # If no phase is provided, return the unfiltered data

    filtered_trials = []
    missing_phase_count = 0

    for trial in trials_data:
        trial_phase = trial.get('phase')
        
        if trial_phase is None:
            missing_phase_count += 1
            logging.warning(f"Trial missing 'phase' key: {trial}")
            continue
        
        if trial_phase.lower() == phase.lower():
            filtered_trials.append(trial)
    
    logging.info(f"Filtered {len(filtered_trials)} trials for phase '{phase}'.")
    if missing_phase_count > 0:
        logging.info(f"{missing_phase_count} trials were missing phase information and were excluded.")

    return filtered_trials

def filter_by_date(trials_data, start_date=None, end_date=None):
    """Filter trials data by a date range."""
    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            logging.error(f"Invalid start date format: {start_date}. Expected format is YYYY-MM-DD.")
            return []

    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            logging.error(f"Invalid end date format: {end_date}. Expected format is YYYY-MM-DD.")
            return []

    filtered_trials = []
    for trial in trials_data:
        try:
            trial_date = datetime.strptime(trial['date'], "%Y-%m-%d")
        except (KeyError, ValueError):
            logging.warning(f"Skipping trial due to invalid or missing date: {trial}")
            continue
        
        if start_date and trial_date < start_date:
            continue
        if end_date and trial_date > end_date:
            continue
        filtered_trials.append(trial)
    
    logging.info(f"Filtered {len(filtered_trials)} trials based on the provided date range.")
    return filtered_trials

if __name__ == "__main__":
    # Example trials data
    example_trials_data = [
        {"id": 1, "phase": "Phase I"},
        {"id": 2, "phase": "Phase II"},
        {"id": 3, "name": "Trial without phase"},
        {"id": 4, "phase": "Phase II"},
        {"id": 5, "phase": "Phase I"},
    ]
    
    # Filter by a specific phase
    filtered = filter_by_phase(example_trials_data, "Phase II")
    print(f"Filtered trials: {filtered}")
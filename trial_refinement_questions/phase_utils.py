# ./trial_refinement_questions/phase_utils.py
from logging_config import logger

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

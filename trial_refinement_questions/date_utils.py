# ./trial_refinement_questions/date_utils.py
from datetime import datetime
from logging_config import logger
import json

def find_status_module(trial):
    """
    Walk through the trial data to find the 'statusModule'.
    
    Args:
        trial (dict): The trial data to search through.
    
    Returns:
        dict: The 'statusModule' if found, otherwise None.
    """
    if isinstance(trial, dict):
        if 'statusModule' in trial:
            return trial['statusModule']
        else:
            for key, value in trial.items():
                if isinstance(value, dict):
                    result = find_status_module(value)
                    if result:
                        return result
                elif isinstance(value, list):
                    for item in value:
                        result = find_status_module(item)
                        if result:
                            return result
    return None

def extract_dates_from_status_module(status_module):
    """
    Extract the start and end dates from the 'statusModule'.
    
    Args:
        status_module (dict): The 'statusModule' from which to extract dates.
    
    Returns:
        tuple: A tuple containing the start date and end date as strings.
    """
    start_date = status_module.get('startDateStruct', {}).get('date')
    end_date = status_module.get('completionDateStruct', {}).get('date')
    
    if not start_date or not end_date:
        logger.warning(f"Missing start or end date in statusModule: {status_module}")
    
    return start_date, end_date

def validate_date_format(date_str):
    """
    Validate and convert a date string to a datetime object.
    
    Args:
        date_str (str): The date string to validate.
    
    Returns:
        datetime: The corresponding datetime object, or None if invalid.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        logger.error(f"Invalid date format: {date_str}. Expected format is YYYY-MM-DD.")
        return None

def filter_by_date(trials_data, start_date=None, end_date=None):
    """
    Filter trials data by a date range after extracting dates from the statusModule.
    
    Args:
        trials_data (list): The list of trial data.
        start_date (str): The start date to filter by.
        end_date (str): The end date to filter by.
    
    Returns:
        list: A list of filtered trials.
    """
    filtered_trials = []
    
    # Convert input dates to datetime objects
    start_date = validate_date_format(start_date)
    end_date = validate_date_format(end_date)
    
    for trial in trials_data:
        status_module = find_status_module(trial)
        if not status_module:
            logger.warning(f"Status Module not found in trial: {trial}")
            continue

        trial_start_date, trial_end_date = extract_dates_from_status_module(status_module)
        trial_start_date = validate_date_format(trial_start_date)
        trial_end_date = validate_date_format(trial_end_date)
        
        if not trial_start_date or not trial_end_date:
            logger.warning(f"Skipping trial due to missing or invalid dates: {trial}")
            continue

        # Check if trial dates fall within the specified range
        if start_date and trial_start_date < start_date:
            continue
        if end_date and trial_end_date > end_date:
            continue
        
        filtered_trials.append(trial)
    
    logger.info(f"Filtered {len(filtered_trials)} trials based on the provided date range.")
    
    # Log the filtered data in detail
    logger.info(f"Filtered data: {json.dumps(filtered_trials, indent=2)}")
    
    return filtered_trials

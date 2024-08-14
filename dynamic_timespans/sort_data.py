# ./sort_data.py
import logging

def sort_by_days_until_end(trials):
    for trial in trials:
        if "daysUntilEnd" not in trial:
            logging.warning(f"Trial {trial.get('nctNumber', 'Unknown')} is missing 'daysUntilEnd'.")
        elif trial["daysUntilEnd"] is None:
            logging.warning(f"Trial {trial.get('nctNumber', 'Unknown')} has 'daysUntilEnd' set to None.")
        elif not isinstance(trial["daysUntilEnd"], int):
            logging.warning(f"Trial {trial.get('nctNumber', 'Unknown')} has an invalid 'daysUntilEnd' value: {trial['daysUntilEnd']}.")

    # Sort, assigning a default high value (infinity) to None or missing 'daysUntilEnd' values
    return sorted(trials, key=lambda x: x["daysUntilEnd"] if isinstance(x["daysUntilEnd"], int) else float('inf'))

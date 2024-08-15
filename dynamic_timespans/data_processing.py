# ./dynamic_timespans/data_processing.py


import os
import sys
import logging
from datetime import datetime


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'tools')))


logging.basicConfig(level=logging.DEBUG)



def process_data(data):
    # Assuming data is a list of trial dictionaries
    processed_data = []
    for trial in data:
        # Example processing: Calculate days until end if not already present
        if 'daysUntilEnd' not in trial:
            if 'startDate' in trial and 'completionDate' in trial:
                trial['daysUntilEnd'] = calculate_days_until_end(trial)
        processed_data.append(trial)
    return processed_data

def calculate_days_until_end(trial):
    # Assuming 'trial' is a dictionary with necessary fields
    start_date = datetime.strptime(trial['startDate'], '%Y-%m-%d')
    end_date = datetime.strptime(trial['completionDate']['date'], '%Y-%m-%d')
    days_until_end = (end_date - start_date).days
    logging.debug(f"Trial {trial['nctNumber']} - Days until end: {days_until_end}")
    return days_until_end



def compare_trials(original_data, output_data):
    missing_days_until_end = set()
    extra_days_until_end = set()

    original_days = set()
    output_days = set()

    for original in original_data:
        if 'daysUntilEnd' in original:
            original_days.add(original['daysUntilEnd'])

    for output in output_data:
        for group in output:
            for trial in group['nctNumbers']:
                output_days.update(trial.values())

    missing_days_until_end = original_days - output_days
    extra_days_until_end = output_days - original_days

    if missing_days_until_end or extra_days_until_end:
        logging.error(f"Days Until End mismatch:\nMissing in output: {missing_days_until_end}\nExtra in output: {extra_days_until_end}")
        raise ValueError(f"Days Until End mismatch:\nMissing in output: {missing_days_until_end}\nExtra in output: {extra_days_until_end}")
    else:
        print("All Days Until End values match between original and output data.")

    print(f"Original Days Until End: {original_days}")
    print(f"Output Days Until End: {output_days}")

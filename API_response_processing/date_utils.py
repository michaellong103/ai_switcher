# ./API_response_processing/date_utils.py
from datetime import datetime
import logging

def calculate_duration_days(start_date_str, end_date_str):
    if not start_date_str or not end_date_str:
        logging.warning(f"Missing start or end date. Start date: '{start_date_str}', End date: '{end_date_str}'")
        return None
    date_formats = ['%Y-%m-%d', '%Y-%m', '%Y']
    start_date, end_date = (None, None)
    for date_format in date_formats:
        try:
            start_date = datetime.strptime(start_date_str, date_format)
            break
        except ValueError:
            continue
    for date_format in date_formats:
        try:
            end_date = datetime.strptime(end_date_str, date_format)
            break
        except ValueError:
            continue
    if start_date and end_date:
        duration_days = (end_date - start_date).days
        logging.debug(f"Duration between '{start_date_str}' and '{end_date_str}' is {duration_days} days.")
        return duration_days
    else:
        logging.warning(f"Date parsing error: Could not parse start or end date. Start date: '{start_date_str}', End date: '{end_date_str}'")
        return None

def calculate_days_until_end(end_date_str):
    if not end_date_str:
        logging.warning(f"Missing end date: '{end_date_str}'")
        return None
    date_formats = ['%Y-%m-%d', '%Y-%m', '%Y']
    end_date = None
    for date_format in date_formats:
        try:
            end_date = datetime.strptime(end_date_str, date_format)
            break
        except ValueError:
            continue
    if end_date:
        current_date = datetime.now()
        days_until_end = (end_date - current_date).days
        logging.debug(f"Days until end date '{end_date_str}': {days_until_end}")
        return days_until_end
    else:
        logging.warning(f'Failed to parse end date: {end_date_str}')
        return None

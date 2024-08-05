# ./date_utils.py

from datetime import datetime
import logging


def calculate_duration_days(start_date_str, end_date_str):
    """
    Calculates the duration in days between two dates.

    Args:
        start_date_str (str): Start date string.
        end_date_str (str): End date string.

    Returns:
        int or None: Duration in days, or None if dates are invalid.
    """
    if not start_date_str or not end_date_str:
        logging.error(f"Missing start or end date. Start date: '{start_date_str}', End date: '{end_date_str}'")
        return None

    date_format = "%Y-%m-%d"
    try:
        logging.debug(f"Parsing start date: '{start_date_str}', end date: '{end_date_str}'")
        start_date = datetime.strptime(start_date_str, date_format)
        end_date = datetime.strptime(end_date_str, date_format)
        duration_days = (end_date - start_date).days
        return duration_days
    except ValueError as e:
        logging.error(f"Date parsing error: {e}")
        return None


def calculate_days_until_end(end_date_str):
    """
    Calculates the number of days until the end date from today.

    Args:
        end_date_str (str): End date string.

    Returns:
        int or None: Days until end, or None if the end date is invalid.
    """
    if not end_date_str:
        logging.error(f"Missing end date: '{end_date_str}'")
        return None

    date_formats = ["%Y-%m-%d", "%Y-%m", "%Y"]
    for date_format in date_formats:
        try:
            logging.debug(f"Parsing end date: '{end_date_str}' with format: '{date_format}'")
            end_date = datetime.strptime(end_date_str, date_format)
            current_date = datetime.now()
            days_until_end = (end_date - current_date).days
            return days_until_end
        except ValueError:
            continue
    logging.error(f"Failed to parse end date: {end_date_str}")
    return None

# ./dynamic_timespans/date_utils.py
from datetime import datetime

CURRENT_DATE = datetime(2024, 7, 16)

def calculate_days_until_end(completion_date_str):
    for fmt in ("%Y-%m-%d", "%Y-%m"):
        try:
            completion_date = datetime.strptime(completion_date_str, fmt)
            delta = (completion_date - CURRENT_DATE).days
            return delta
        except ValueError:
            continue
    raise ValueError(f"Date {completion_date_str} does not match expected formats.")

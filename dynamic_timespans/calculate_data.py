# ./dynamic_timespans/calculate_data.py

from datetime import datetime, timedelta

CURRENT_DATE = datetime(2024, 7, 16)

def calculate_group_data(groups):
    result = []
    for group in groups:
        group_name = group.get("group_name")
        trials = group.get("trials")
        total_trials = len(trials)
        
        if total_trials == 0:
            continue

        nct_numbers = []
        group_dates = []
        for trial in trials:
            nct_number = trial["nctNumber"]
            completion_date = trial["completionDate"]["date"]
            days_until_end = trial["daysUntilEnd"]
            human_readable_date = format_date(completion_date)

            nct_numbers.append({
                nct_number: {
                    "date": completion_date,
                    "daysUntilEnd": days_until_end,
                    "humanReadableDate": human_readable_date
                }
            })
            group_dates.append(parse_date(completion_date))

        earliest_date = min(group_dates)
        latest_date = max(group_dates)

        earliest_date_str = format_date(earliest_date.strftime("%Y-%m-%d"))
        latest_date_str = format_date(latest_date.strftime("%Y-%m-%d"))

        earliest_date_from_today = calculate_date_from_today(earliest_date)
        latest_date_from_today = calculate_date_from_today(latest_date)

        result.append({
            "total": total_trials,
            "nctNumbers": nct_numbers,
            "trialGroup": group_name,
            "dateSpan": calculate_date_span(trials),
            "dateSpan2": calculate_date_span2(trials),
            "earliestDate": earliest_date_str,
            "latestDate": latest_date_str,
            "earliestDateFromToday": earliest_date_from_today,
            "latestDateFromToday": latest_date_from_today
        })
    return result

def format_date(date_str):
    try:
        if len(date_str) == 7:  # Format: YYYY-MM
            year, month = map(int, date_str.split('-'))
            last_day_of_month = (datetime(year, month, 1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            return last_day_of_month.strftime("%d %B %Y")
        elif len(date_str) == 10:  # Format: YYYY-MM-DD
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d %B %Y")
    except ValueError as e:
        print(f"Error parsing date {date_str}: {e}")
    return "Unknown"

def parse_date(date_str):
    try:
        if len(date_str) == 7:  # Format: YYYY-MM
            year, month = map(int, date_str.split('-'))
            return (datetime(year, month, 1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        elif len(date_str) == 10:  # Format: YYYY-MM-DD
            return datetime.strptime(date_str, "%Y-%m-%d")
        elif len(date_str.split()) == 3:  # Format: DD Month YYYY
            return datetime.strptime(date_str, "%d %B %Y")
        else:
            print(f"Unrecognized date format: {date_str}")
    except ValueError as e:
        print(f"Error parsing date {date_str}: {e}")
    return None
def calculate_date_span(trials):
    days_until_end_list = [trial["daysUntilEnd"] for trial in trials]
    return max(days_until_end_list) - min(days_until_end_list)

def calculate_date_span2(trials):
    days_until_end_list = [trial["daysUntilEnd"] for trial in trials]
    return f"{min(days_until_end_list)} days to {max(days_until_end_list)} days"

def calculate_date_from_today(target_date, show_months=True):
    delta = target_date - CURRENT_DATE
    years = delta.days // 365
    remaining_days = delta.days % 365
    months = remaining_days // 30
    
    # Rounding logic
    if months >= 6:
        years += 1
        months = 0
    
    result = []
    if years > 0:
        result.append(f"{years} year{'s' if years > 1 else ''}")
    if show_months and months > 0:
        result.append(f"{months} month{'s' if months > 1 else ''}")
    
    return " ".join(result) if result else "0 months"

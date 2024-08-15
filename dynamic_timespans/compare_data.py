# ./dynamic_timespans/compare_data.py
def compare_sorted_data(sorted_trials, original_trials):
    sorted_days_until_end = [trial["daysUntilEnd"] for trial in sorted_trials]
    original_days_until_end = [trial["daysUntilEnd"] for trial in original_trials]
    
    if sorted_days_until_end == sorted(original_days_until_end):
        print("Data is correctly sorted.")
    else:
        print("Data sorting has discrepancies.")

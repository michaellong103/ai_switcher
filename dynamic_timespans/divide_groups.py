# ./divide_groups.py
def divide_into_groups(trials):
    total_trials = len(trials)
    groups = []

    # Sort trials by completion date to ensure chronological order
    sorted_trials = sorted(trials, key=lambda x: x["completionDate"]["date"])

    if 15 <= total_trials <= 28:
        num_groups = 2
    elif 29 <= total_trials <= 40:
        num_groups = 3
    elif 41 <= total_trials <= 50:
        num_groups = 4
    elif 51 <= total_trials <= 60:
        num_groups = 5
    elif total_trials > 60:
        num_groups = 6
    else:
        num_groups = 1

    trials_per_group = total_trials // num_groups
    remainder = total_trials % num_groups

    start_index = 0
    for i in range(num_groups):
        end_index = start_index + trials_per_group + (1 if i < remainder else 0)
        group_trials = sorted_trials[start_index:end_index]
        groups.append({
            "group_name": f"Group {i + 1}",
            "trials": group_trials
        })
        start_index = end_index

    return groups

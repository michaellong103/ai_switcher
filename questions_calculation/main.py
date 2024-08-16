import json
import numpy as np

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def find_best_group_in_times_json(times_data):
    """Find the largest group in times_question_output.json that is closest to but does not exceed 10 trials."""
    best_group = None
    closest_count = 0
    trial_counts = []
    num_groups = 0

    if isinstance(times_data, list):
        for group in times_data:
            trial_count = group['total']
            trial_counts.append(trial_count)
            num_groups += 1
            print(f"Group '{group['trialGroup']}' has {trial_count} trials.")
            if 0 < trial_count <= 10 and trial_count > closest_count:
                closest_count = trial_count
                best_group = group

    print(f"Total number of groups in 'times_question_output.json': {num_groups}")
    return best_group, closest_count, trial_counts

def find_best_group_in_phase_json(phase_data):
    """Find the largest group in phase_question_output.json that is closest to but does not exceed 10 trials."""
    best_group = None
    closest_count = 0
    trial_counts = []
    num_groups = 0

    if 'options' in phase_data:
        for option in phase_data['options']:
            trial_counts.append(option['NCTCount'])
            num_groups += 1
            print(f"Group '{option['optionText']}' has {option['NCTCount']} trials.")
            if 0 < option['NCTCount'] <= 10 and option['NCTCount'] > closest_count:
                closest_count = option['NCTCount']
                best_group = option

    print(f"Total number of groups in 'phase_question_output.json': {num_groups}")
    return best_group, closest_count, trial_counts

def calculate_mad(trial_counts):
    """Calculate the Mean Absolute Deviation (MAD) for a list of trial counts."""
    if len(trial_counts) == 0:
        return None, None
    mean = np.mean(trial_counts)
    deviations = [abs(x - mean) for x in trial_counts]
    mad = np.mean(deviations)
    return mad, mean

def print_group_info(group, group_name, source_file, count):
    """Print the group name, source file, and count in green."""
    green_text = "\033[92m"  # ANSI escape code for green text
    reset_text = "\033[0m"   # ANSI escape code to reset text color

    print(f"{green_text}Group: {group_name} from {source_file} with {count} trials{reset_text}")

def main():
    # Load JSON data
    times_data = load_json('../API_response/times_question_output.json')
    phase_data = load_json('../API_response/phase_question_output.json')

    # Find the best group in each JSON file and collect trial counts for calculations
    best_times_group, times_group_trials, times_trial_counts = find_best_group_in_times_json(times_data)
    best_phase_group, phase_group_trials, phase_trial_counts = find_best_group_in_phase_json(phase_data)

    # Calculate MAD and average for each file
    times_mad, times_mean = calculate_mad(times_trial_counts)
    phase_mad, phase_mean = calculate_mad(phase_trial_counts)

    # Determine which group is the best overall and print it
    if best_times_group and best_phase_group:
        if times_group_trials >= phase_group_trials:
            print_group_info(best_times_group, best_times_group['trialGroup'], "times_question_output.json", times_group_trials)
        else:
            print_group_info(best_phase_group, best_phase_group['optionText'], "phase_question_output.json", phase_group_trials)
    elif best_times_group:
        print_group_info(best_times_group, best_times_group['trialGroup'], "times_question_output.json", times_group_trials)
    elif best_phase_group:
        print_group_info(best_phase_group, best_phase_group['optionText'], "phase_question_output.json", phase_group_trials)
    else:
        print("No valid group found in either file.")

    # Print the detailed statistics for 'times_question_output.json'
    if times_mad is not None:
        print(f"\nTotal Trials in Calculation: {sum(times_trial_counts)}")
        print(f"Average: {times_mean:.2f}")
        print(f"Mean Absolute Deviation (MAD) for 'times_question_output.json': {times_mad:.2f}")
    else:
        print("\nMean Absolute Deviation (MAD) for 'times_question_output.json': No valid data")

    # Print the detailed statistics for 'phase_question_output.json'
    if phase_mad is not None:
        print(f"\nTotal Trials in Calculation: {sum(phase_trial_counts)}")
        print(f"Average: {phase_mean:.2f}")
        print(f"Mean Absolute Deviation (MAD) for 'phase_question_output.json': {phase_mad:.2f}")
    else:
        print("Mean Absolute Deviation (MAD) for 'phase_question_output.json': No valid data")

if __name__ == "__main__":
    main()

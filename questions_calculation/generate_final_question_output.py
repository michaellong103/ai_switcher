# ./generate_final_question_output.py
import json
from utils import (
    load_json,
    find_best_group_in_times_json,
    find_best_group_in_phase_json,
    calculate_mad,
    extract_nct_numbers_from_times,
    extract_nct_numbers_from_phase,
    find_duplicated_trials
)

def print_results_and_generate_output():
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

    # Calculate and print duplicated trials
    times_ncts = extract_nct_numbers_from_times(times_data)
    phase_ncts = extract_nct_numbers_from_phase(phase_data)
    duplicates, num_duplicates = find_duplicated_trials(times_ncts, phase_ncts)

    print(f"\nNumber of duplicated trials between phases: {num_duplicates}")
    if num_duplicates > 0:
        print("List of duplicated trials:")
        print(duplicates)

    # Generate the final JSON output
    final_data = {
        "questions": [
            {
                "question": "times_question_output.json",
                "summary": {
                    "total_trials": sum(times_trial_counts),
                    "average": times_mean,
                    "mad": times_mad
                },
                "data": times_data
            },
            {
                "question": "phase_question_output.json",
                "summary": {
                    "total_trials": sum(phase_trial_counts),
                    "average": phase_mean,
                    "mad": phase_mad,
                    "duplicated_trials": num_duplicates
                },
                "data": phase_data
            }
        ]
    }

    # Write final data to a JSON file
    with open('final_question_output.json', 'w') as json_file:
        json.dump(final_data, json_file, indent=4)
    print("\nFinal JSON output generated: final_question_output.json")

if __name__ == "__main__":
    print_results_and_generate_output()

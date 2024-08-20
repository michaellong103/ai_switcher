# ./questions_calculation/main.py

import os
import json
from utils import (
    load_json,
    find_best_group_in_times_json,
    find_best_group_in_phase_json,
    calculate_mad,
    extract_nct_numbers_from_times,
    extract_nct_numbers_from_phase,
    find_duplicated_trials,
    print_group_info
)

def generate_description(group):
    human_range = f"{group['earliestDateFromToday']} to {group['latestDateFromToday']}"
    return f"{group['trialGroup']} (approximately {human_range})"

def print_results_and_generate_output():
    # Determine the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define file paths using os.path.join for platform independence
    times_file_path = os.path.join(script_dir, '..', 'API_response', 'times_question_output.json')
    phase_file_path = os.path.join(script_dir, '..', 'API_response', 'phase_question_output.json')
    output_file_path = os.path.join(script_dir, '..', 'API_response', 'final_question_output.json')

    # Load JSON data
    times_data = load_json(times_file_path)
    phase_data = load_json(phase_file_path)

    # Find the best group in each JSON file and collect trial counts for calculations
    best_times_group, times_group_trials, times_trial_counts = find_best_group_in_times_json(times_data)
    best_phase_group, phase_group_trials, phase_trial_counts = find_best_group_in_phase_json(phase_data)

    # Calculate MAD and average for each file
    times_mad, times_mean = calculate_mad(times_trial_counts)
    phase_mad, phase_mean = calculate_mad(phase_trial_counts)

    # Round MAD and average values to one decimal place
    times_mad = round(times_mad, 1)
    times_mean = round(times_mean, 1)
    phase_mad = round(phase_mad, 1)
    phase_mean = round(phase_mean, 1)

    # Calculate and print duplicated trials
    times_ncts = extract_nct_numbers_from_times(times_data)
    phase_ncts = extract_nct_numbers_from_phase(phase_data)
    duplicates, num_duplicates = find_duplicated_trials(times_ncts, phase_ncts)

    # Generate the final JSON output with dynamically generated descriptions
    final_data = {
        "qs": [
            {
                "q": "How long are you willing to commit to a clinical trial? ({} Trials Available)".format(sum(times_trial_counts)),
                "sum": {
                    "tot_trials": sum(times_trial_counts),
                    "avg": times_mean,
                    "mad": times_mad
                },
                "data": [
                    {
                        "tot": group["total"],
                        "NCTn": [
                            {
                                nct: {
                                    "d": details["date"],
                                    "dEnd": details["daysUntilEnd"],
                                    "hDate": details["humanReadableDate"]
                                } for nct, details in nct_dict.items()
                            } for nct_dict in group["nctNumbers"]
                        ],
                        "grp": generate_description(group)  # Updated description without days range
                    } for group in times_data
                ]
            },
            {
                "q": "Which phase of clinical trials are you comfortable participating in? ({} Trials Available)".format(sum(phase_trial_counts)),
                "sum": {
                    "tot_trials": sum(phase_trial_counts),
                    "avg": phase_mean,
                    "mad": phase_mad,
                    "dup_trials": num_duplicates
                },
                "data": {
                    "opts": [
                        {
                            "NCTc": option["NCTCount"],
                            "opt_txt": option["optionText"] + ": " + option.get("description", ""),
                            "NCTn": option["NCTNumbers"]
                        } for option in phase_data.get("options", [])
                    ]
                }
            }
        ]
    }

    # Write final data to a JSON file in the specified output path
    with open(output_file_path, 'w') as json_file:
        json.dump(final_data, json_file, indent=4)
    print(f"\nFinal JSON output generated: {output_file_path}")

if __name__ == "__main__":
    print_results_and_generate_output()

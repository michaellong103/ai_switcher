# ./data_cleaning.py

import os
import re

try:
    from .date_utils import calculate_duration_days, calculate_days_until_end
    from .file_utils import save_json_to_file
except ImportError:
    from date_utils import calculate_duration_days, calculate_days_until_end
    from file_utils import save_json_to_file


def split_eligibility_criteria(eligibility):
    """
    Splits eligibility criteria into inclusion and exclusion sections.

    Args:
        eligibility (str): The eligibility criteria text.

    Returns:
        dict: A dictionary with inclusion and exclusion criteria.
    """
    pattern = re.compile(r'(Inclusion Criteria|Exclusion Criteria):?\n\n?', re.IGNORECASE)
    split_criteria = pattern.split(eligibility)

    criteria = {"InclusionCriteria": "", "ExclusionCriteria": ""}

    if len(split_criteria) > 1:
        for i in range(1, len(split_criteria), 2):
            section_title = split_criteria[i].lower()
            section_text = split_criteria[i + 1].strip()
            if 'inclusion' in section_title:
                criteria["InclusionCriteria"] = section_text
            elif 'exclusion' in section_title:
                criteria["ExclusionCriteria"] = section_text

    return criteria


def clean_study_data(studies, output_dir):
    """
    Cleans and processes study data.

    Args:
        studies (list): List of study data dictionaries.
        output_dir (str): Directory to save cleaned data.

    Returns:
        list: A list of cleaned study data.
    """
    cleaned_studies = []
    for study in studies:
        study_info = study.get('protocolSection', {})
        nct_id = study_info.get('identificationModule', {}).get('nctId', '')
        eligibility_criteria = study_info.get("eligibilityModule", {}).get("eligibilityCriteria", "")

        criteria = split_eligibility_criteria(eligibility_criteria)
        cleaned_study = {
            "EligibilityCriteria": eligibility_criteria,
            "InclusionCriteria": criteria["InclusionCriteria"],
            "ExclusionCriteria": criteria["ExclusionCriteria"],
            "HealthyVolunteers": study_info.get("eligibilityModule", {}).get("healthyVolunteers", ""),
            "Gender": study_info.get("eligibilityModule", {}).get("sex", ""),
            "MinimumAge": study_info.get("eligibilityModule", {}).get("minimumAge", ""),
            "NCTId": nct_id,
            "startDate": study_info.get("statusModule", {}).get("startDateStruct", {}).get("startDate", ""),
            "completionDate": study_info.get("statusModule", {}).get("completionDateStruct", {}).get("completionDate", "")
        }

        start_date_str = cleaned_study["startDate"]
        completion_date_str = cleaned_study["completionDate"]
        cleaned_study["durationDays"] = calculate_duration_days(start_date_str, completion_date_str)
        cleaned_study["daysUntilEnd"] = calculate_days_until_end(completion_date_str)

        cleaned_studies.append(cleaned_study)

    cleaned_file_path = os.path.join(output_dir, 'cleaned_data.json')
    save_json_to_file(cleaned_studies, cleaned_file_path, "Cleaned data")
    return cleaned_studies


def filter_exclusion_criteria_and_write(cleaned_data, output_dir):
    """
    Filters exclusion criteria and writes filtered data to a file.

    Args:
        cleaned_data (list): List of cleaned study data.
        output_dir (str): Directory to save filtered data.
    """
    filtered_data = [
        {
            "ExclusionCriteria": f"(exclusion criteria not marked) {study['EligibilityCriteria']}" if not study["ExclusionCriteria"] else study["ExclusionCriteria"],
            "NCTId": study["NCTId"]
        }
        for study in cleaned_data
    ]

    filtered_file_path = os.path.join(output_dir, 'filtered_exclusion_data.json')
    save_json_to_file(filtered_data, filtered_file_path, "Filtered data")


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 3:
        print("Usage: python data_cleaning.py <input_json_file> <output_dir>")
        sys.exit(1)

    # Dynamic path construction
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_json_file = os.path.join(script_dir, sys.argv[1])
    output_dir = os.path.join(script_dir, sys.argv[2])

    with open(input_json_file, 'r') as file:
        trials_data = json.load(file)

    cleaned_data = clean_study_data(trials_data, output_dir)
    filter_exclusion_criteria_and_write(cleaned_data, output_dir)

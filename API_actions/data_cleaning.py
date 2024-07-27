# ./API_actions/data_cleaning.py

import json
import os
import re
import logging
from datetime import datetime

def split_eligibility_criteria(eligibility):
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

def calculate_duration_days(start_date_str, end_date_str):
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


def filter_exclusion_criteria_and_write(cleaned_data, output_dir):
    filtered_data = [
        {
            "ExclusionCriteria": f"(exclusion criteria not marked) {study['EligibilityCriteria']}" if not study["ExclusionCriteria"] else study["ExclusionCriteria"],
            "NCTId": study["NCTId"]
        }
        for study in cleaned_data
    ]

    filtered_file_path = os.path.join(output_dir, 'filtered_exclusion_data.json')
    save_json_to_file(filtered_data, filtered_file_path, "Filtered data")
    
def extract_clinical_trial_info(trial_data, output_dir):
    extracted_data = []
    for trial in trial_data:
        study_info = trial.get("protocolSection", {})
        start_date_str = study_info.get("statusModule", {}).get("startDateStruct", {}).get("date", "")
        completion_date_str = study_info.get("statusModule", {}).get("completionDateStruct", {}).get("date", "")
        
        def parse_date(date_str):
            date_formats = ["%B %d, %Y", "%Y-%m-%d", "%Y-%m", "%Y"]
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            return None
        
        start_date = parse_date(start_date_str)
        completion_date = parse_date(completion_date_str)
        duration_days = (completion_date - start_date).days if start_date and completion_date else None
        
        extracted_info = {
            "trialName": study_info.get("identificationModule", {}).get("officialTitle", ""),
            "nctNumber": study_info.get("identificationModule", {}).get("nctId", ""),
            "status": study_info.get("statusModule", {}).get("overallStatus", ""),
            "studyType": study_info.get("designModule", {}).get("studyType", ""),
            "studyPhases": study_info.get("designModule", {}).get("phases", []),
            "primaryCompletionDate": study_info.get("statusModule", {}).get("primaryCompletionDateStruct", {}),
            "completionDate": study_info.get("statusModule", {}).get("completionDateStruct", {}),
            "startDate": start_date_str,
            "startDateType": study_info.get("statusModule", {}).get("startDateStruct", {}).get("type", ""),
            "durationDays": duration_days,  # New field for duration in days
            "daysUntilEnd": calculate_days_until_end(completion_date_str)  # New field for days until end of the trial
        }
        extracted_data.append(extracted_info)

    extracted_file_path = os.path.join(output_dir, 'extracted_data.json')
    save_json_to_file(extracted_data, extracted_file_path, "Extracted data")
    return extracted_data

def save_json_to_file(data, path, description):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)
    logging.debug(f"{description} saved to '{path}'")

def load_json_from_file(path):
    with open(path, 'r') as file:
        return json.load(file)

def save_all_study_data(studies, output_dir):
    all_data_file_path = os.path.join(output_dir, 'all_study_data.json')
    save_json_to_file(studies, all_data_file_path, "All data")

if __name__ == "__main__":
    trials_data = load_json_from_file('path_to_your_json_file.json')
    output_dir = 'your_output_directory'
    extracted_data = extract_clinical_trial_info(trials_data, output_dir)
    cleaned_data = clean_study_data(trials_data, output_dir)
    filter_exclusion_criteria_and_write(cleaned_data, output_dir)
    save_all_study_data(trials_data, output_dir)

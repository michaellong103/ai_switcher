# ./clinical_trial_processor.py
import os
import json
from datetime import datetime, timedelta

try:
    from .file_utils import save_json_to_file
except ImportError:
    from file_utils import save_json_to_file

INPUT_FILE = os.path.join(os.path.dirname(__file__), "../API_response/finaloutput.json")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "../API_response/dynamic_questions_input.json")

def parse_date(date_str):
    print(f"Attempting to parse date: {date_str}")
    date_formats = ["%B %d, %Y", "%Y-%m-%d", "%Y-%m", "%Y"]
    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            print(f"Successfully parsed date '{date_str}' with format '{fmt}': {parsed_date}")
            return parsed_date
        except ValueError:
            print(f"Failed to parse date '{date_str}' with format '{fmt}'")
            continue
    
    # Handle cases where only a year or year and month are provided
    if len(date_str) == 7:  # Format YYYY-MM
        try:
            parsed_date = datetime.strptime(date_str, "%Y-%m")
            print(f"Assuming end of month for date '{date_str}': {parsed_date}")
            return parsed_date + timedelta(days=30)  # Assume end of month
        except ValueError:
            print(f"Failed to parse partial date '{date_str}' with format 'YYYY-MM'")
    elif len(date_str) == 4:  # Format YYYY
        parsed_date = datetime.strptime(date_str, "%Y")
        print(f"Assuming beginning of year for date '{date_str}': {parsed_date}")
        return parsed_date
    
    print(f"Returning None for unrecognized date format: {date_str}")
    return None

def calculate_days_until_end(completion_date_str):
    print(f"Calculating days until end for completion date: {completion_date_str}")
    completion_date = parse_date(completion_date_str)
    if not completion_date:
        print(f"Completion date parsing failed or is None. Returning None.")
        return None
    
    today = datetime.today()
    days_until_end = (completion_date - today).days
    print(f"Days until end: {days_until_end} (Today: {today}, Completion Date: {completion_date})")
    return days_until_end

def extract_clinical_trial_info(trial_data):
    extracted_data = []
    for trial in trial_data:
        if isinstance(trial, dict):
            study_info = trial.get("protocolSection", {})
            start_date_str = study_info.get("statusModule", {}).get("startDateStruct", {}).get("date", "")
            completion_date_str = study_info.get("statusModule", {}).get("completionDateStruct", {}).get("date", "")
            
            print(f"Processing trial: {study_info.get('identificationModule', {}).get('officialTitle', 'Unknown Title')}")
            print(f"Start Date: {start_date_str}, Completion Date: {completion_date_str}")
            
            start_date = parse_date(start_date_str)
            completion_date = parse_date(completion_date_str)
            duration_days = (completion_date - start_date).days if start_date and completion_date else None
            print(f"Duration Days: {duration_days}")
            
            days_until_end = calculate_days_until_end(completion_date_str)
            print(f"Final Days Until End: {days_until_end}")
            
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
                "durationDays": duration_days,
                "daysUntilEnd": days_until_end
            }
            extracted_data.append(extracted_info)

    return extracted_data

def process_clinical_trials(input_file, output_file):
    print(f"Processing clinical trials from input file: {input_file}")
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    trial_data = data.get("studies", [])
    if not trial_data:
        print("No trial data found in the input file.")
        return
    
    extracted_data = extract_clinical_trial_info(trial_data)
    print(f"Saving extracted data to output file: {output_file}")
    save_json_to_file(extracted_data, output_file, "Extracted clinical trial data")

def run_processing():
    process_clinical_trials(INPUT_FILE, OUTPUT_FILE)

if __name__ == "__main__":
    run_processing()

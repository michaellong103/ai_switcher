# ./data_extraction.py
import os
from datetime import datetime
import logging
try:
    from .date_utils import calculate_days_until_end
    from .file_utils import save_json_to_file
except ImportError:
    from date_utils import calculate_days_until_end
    from file_utils import save_json_to_file

def parse_date(date_str):
    date_formats = ['%B %d, %Y', '%Y-%m-%d', '%Y-%m', '%Y']
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    logging.debug(f'Failed to parse date: {date_str}')
    return None

def extract_clinical_trial_info(trial_data, output_dir):
    extracted_data = []
    for trial in trial_data:
        nct_id = trial.get('protocolSection', {}).get('identificationModule', {}).get('nctId', 'Unknown')
        logging.debug(f'Processing trial with NCT ID: {nct_id}')
        study_info = trial.get('protocolSection', {})
        status_module = study_info.get('statusModule', {})
        status_verified_date = status_module.get('statusVerifiedDate', '')
        overall_status = status_module.get('overallStatus', '')
        start_date_str = status_module.get('startDateStruct', {}).get('date', '')
        primary_completion_date_str = status_module.get('primaryCompletionDateStruct', {}).get('date', '')
        completion_date_str = status_module.get('completionDateStruct', {}).get('date', '')
        study_first_submit_date = status_module.get('studyFirstSubmitDate', '')
        last_update_submit_date = status_module.get('lastUpdateSubmitDate', '')
        duration_days = None
        days_until_end = None
        if not start_date_str:
            logging.warning(f'Missing start date for trial with NCT ID: {nct_id}. JSON path: statusModule.startDateStruct.date')
        if not completion_date_str:
            logging.warning(f'Missing completion date for trial with NCT ID: {nct_id}. JSON path: statusModule.completionDateStruct.date')
        if start_date_str and completion_date_str:
            start_date = parse_date(start_date_str)
            completion_date = parse_date(completion_date_str)
            if start_date and completion_date:
                duration_days = (completion_date - start_date).days
                days_until_end = calculate_days_until_end(completion_date_str)
            else:
                logging.warning(f'Unable to parse one or both dates for trial with NCT ID: {nct_id}. Start: {start_date_str}, End: {completion_date_str}')
        extracted_info = {'trialName': study_info.get('identificationModule', {}).get('officialTitle', ''), 'nctNumber': nct_id, 'statusVerifiedDate': status_verified_date, 'overallStatus': overall_status, 'startDate': start_date_str, 'primaryCompletionDate': primary_completion_date_str, 'completionDate': completion_date_str, 'studyFirstSubmitDate': study_first_submit_date, 'lastUpdateSubmitDate': last_update_submit_date, 'startDateType': status_module.get('startDateStruct', {}).get('type', ''), 'durationDays': duration_days, 'daysUntilEnd': days_until_end}
        extracted_data.append(extracted_info)
    extracted_file_path = os.path.join(output_dir, 'extracted_data.json')
    save_json_to_file(extracted_data, extracted_file_path, 'Extracted data')
    return extracted_data
if __name__ == '__main__':
    import sys
    import json
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    if len(sys.argv) < 3:
        logging.error('Usage: python data_extraction.py <input_json_file> <output_dir>')
        sys.exit(1)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_json_file = os.path.join(script_dir, sys.argv[1])
    output_dir = os.path.join(script_dir, sys.argv[2])
    try:
        with open(input_json_file, 'r') as file:
            trials_data = json.load(file)['studies']
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        logging.error(f'Failed to load JSON data: {e}')
        sys.exit(1)
    extract_clinical_trial_info(trials_data, output_dir)

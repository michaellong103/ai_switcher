# ./assistants/medical/validator_utils.py
import re
import json
import logging
with open('assistants/medical/conditions_incomplete.json', 'r') as f:
    conditions_data = json.load(f)
    conditions = conditions_data['conditions']
incomplete_keywords_pattern = re.compile('\\bincomplete\\b|\\bmissing\\b|\\bmore info needed\\b', re.IGNORECASE)
special_characters_pattern = re.compile('[!@#$%^&*()?":{}|<>]')
square_brackets_pattern = re.compile('\\[\\s*\\]')

def validate_medical_condition(response):
    condition_match = re.search('Medical Condition:\\s*([^\\n]+)', response)
    if condition_match:
        condition = condition_match.group(1).strip()
        if condition in conditions:
            return 'The medical condition needs to be more specific.'
        else:
            return 'The data will be submitted with this criteria to find applicable trials.'
    return 'The medical condition needs to be completed.'

def check_special_characters(value):
    return not bool(special_characters_pattern.search(value))

def is_complete_response(response):
    keyword_match = incomplete_keywords_pattern.search(response)
    if keyword_match:
        logging.warning(f'Incomplete keyword found: {keyword_match.group()}')
        return False
    age_match = re.search('Age:\\s*(\\d+)', response)
    gender_match = re.search('Gender:\\s*(\\w+)', response)
    condition_match = re.search('Medical Condition:\\s*([^\\n]+)', response)
    location_match = re.search('Location:\\s*([^\\n]+)', response)
    debug_grid_match = re.search('Debug Grid:\\s*\\[\\(([^,]+),\\s*([^)]+)\\)\\]', response)
    fields = {'Age': age_match, 'Gender': gender_match, 'Medical Condition': condition_match, 'Location': location_match}
    for field, match in fields.items():
        field_value = match.group(1).strip() if match else ''
        logging.info(f'Validating field {field}: {field_value}')
        if not field_value:
            logging.warning(f'Empty field found: {field}')
            return False
        if not check_special_characters(field_value):
            logging.warning(f'Special character found in field {field}: {field_value}')
            return False
    if debug_grid_match:
        latitude = debug_grid_match.group(1).strip()
        longitude = debug_grid_match.group(2).strip()
        logging.info(f'Validating Debug Grid - Latitude: {latitude}, Longitude: {longitude}')
        if not check_special_characters(latitude) or not check_special_characters(longitude):
            logging.warning('Special character found in Debug Grid')
            return False
    return True

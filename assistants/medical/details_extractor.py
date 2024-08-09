# ./assistants/medical/details_extractor.py
import re

def extract_details(text):
    details = {}
    age_match = re.search('Age:\\s*(\\d+)', text)
    gender_match = re.search('Gender:\\s*(\\w+)', text)
    condition_match = re.search('Medical Condition:\\s*([^\\n]+)', text)
    location_match = re.search('Location:\\s*([^\\n]+)', text)
    debug_grid_match = re.search('Debug Grid:\\s*\\[\\(([^,]+),\\s*([^)]+)\\)\\]', text)
    if age_match:
        details['Age'] = age_match.group(1)
    if gender_match:
        details['Gender'] = gender_match.group(1)
    if condition_match:
        details['Medical Condition'] = condition_match.group(1)
    if location_match:
        details['Location'] = location_match.group(1)
    if debug_grid_match:
        details['Latitude'] = debug_grid_match.group(1)
        details['Longitude'] = debug_grid_match.group(2)
    return details

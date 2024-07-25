import re
import json
import logging

with open('assistants/medical/conditions_incomplete.json', 'r') as f:
    conditions_data = json.load(f)
    conditions = conditions_data['conditions']

incomplete_keywords_pattern = re.compile(r'\bincomplete\b|\bmissing\b|\bmore info needed\b', re.IGNORECASE)
special_characters_pattern = re.compile(r'[!@#$%^&*()?":{}|<>]')
square_brackets_pattern = re.compile(r'\[\s*\]')

def validate_medical_condition(response):
    """
    Validates if the medical condition is in the predefined list of common medical conditions.
    
    Parameters:
    response (str): The response text to be checked.
    
    Returns:
    str: A message indicating whether more information is needed or if the field passes.
    """
    # Extract the medical condition from the response
    condition_match = re.search(r'Medical Condition:\s*([^\n]+)', response)
    
    if condition_match:
        condition = condition_match.group(1).strip()
        if condition in conditions:
            return "The medical condition needs to be more specific."
        else:
            return "The data will be submitted with this criteria to find applicable trials."
    return "The medical condition needs to be completed."

def check_special_characters(value):
    """
    Check if the provided value contains any special characters.
    
    Parameters:
    value (str): The value to be checked.
    
    Returns:
    bool: True if no special characters are found, False otherwise.
    """
    return not bool(special_characters_pattern.search(value))

def is_complete_response(response):
    """
    Check if the response is complete based on the absence of incomplete keywords,
    special characters, and empty fields.
    
    Parameters:
    response (str): The response text to be checked.
    
    Returns:
    bool: True if the response is complete, False otherwise.
    """
    # Check if any incomplete keyword is present in the response
    keyword_match = incomplete_keywords_pattern.search(response)
    if keyword_match:
        logging.warning(f"Incomplete keyword found: {keyword_match.group()}")
        return False

    # Extract individual fields
    age_match = re.search(r'Age:\s*(\d+)', response)
    gender_match = re.search(r'Gender:\s*(\w+)', response)
    condition_match = re.search(r'Medical Condition:\s*([^\n]+)', response)
    location_match = re.search(r'Location:\s*([^\n]+)', response)
    debug_grid_match = re.search(r'Debug Grid:\s*\[\(([^,]+),\s*([^)]+)\)\]', response)

    # Check for empty fields and special characters
    fields = {
        "Age": age_match,
        "Gender": gender_match,
        "Medical Condition": condition_match,
        "Location": location_match
    }

    for field, match in fields.items():
        if not match or not match.group(1).strip():
            logging.warning(f"Empty field found: {field}")
            return False
        if not check_special_characters(match.group(1)):
            logging.warning(f"Special character found in field {field}: {match.group(1)}")
            return False

    if debug_grid_match:
        latitude = debug_grid_match.group(1).strip()
        longitude = debug_grid_match.group(2).strip()
        if not check_special_characters(latitude) or not check_special_characters(longitude):
            logging.warning("Special character found in Debug Grid")
            return False

    return True

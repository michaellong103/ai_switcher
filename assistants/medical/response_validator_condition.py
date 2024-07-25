# ./assistants/medical/response_validator_condition.py

import re
import json

# Load conditions from JSON
with open('assistants/medical/conditions_incomplete.json', 'r') as f:
    conditions_data = json.load(f)
    conditions = conditions_data['conditions']

# Define patterns
incomplete_keywords_pattern = re.compile(r'\bincomplete\b|\bmissing\b|\bmore info needed\b', re.IGNORECASE)
special_characters_pattern = re.compile(r'[!@#$%^&*(),.?":{}|<>]')
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


def is_complete_response(response):
    """
    Check if the response is complete based on the absence of incomplete keywords,
    special characters, and empty fields.
    
    Parameters:
    response (str): The response text to be checked.
    
    Returns:
    bool: True if the response is complete, False otherwise.
    """
    # Exclude Debug Grid content for special character detection
    debug_grid_pattern = re.compile(r'Debug Grid: \[\(([^,]+),\s*([^)]+)\)\]')
    cleaned_response = debug_grid_pattern.sub('Debug Grid: []', response)

    # Check if any incomplete keyword is present in the response
    keyword_match = incomplete_keywords_pattern.search(cleaned_response)
    if keyword_match:
        print(f"Incomplete keyword found: {keyword_match.group()}")
        return False

    # Check if any special character is present in the cleaned response
    special_char_match = special_characters_pattern.search(cleaned_response)
    if special_char_match:
        print(f"Special character found: {special_char_match.group()}")
        return False

    # Check if any invalid square brackets are present in the cleaned response
    square_brackets_match = square_brackets_pattern.search(cleaned_response)
    if square_brackets_match:
        print(f"Special character found: {square_brackets_match.group()}")
        return False

    # Check for empty fields
    required_fields = ["Age:", "Gender:", "Medical Condition:", "Location:"]
    for field in required_fields:
        pattern = re.compile(rf'{field}\s*$', re.MULTILINE)
        if pattern.search(response):
            print(f"Empty field found: {field}")
            return False

    return True

def main():
    # Example responses
    response_with_common_condition = """- Age: 50
    - Gender: Female
    - Medical Condition: Common Cold
    - Location: Los Angeles, CA
    - Debug Grid: [(34.0522, -118.2437)]
    
    I will now search for trials that match this profile."""

    response_with_uncommon_condition = """- Age: 50
    - Gender: Female
    - Medical Condition: Rare Disease
    - Location: Los Angeles, CA
    - Debug Grid: [(34.0522, -118.2437)]
    
    I will now search for trials that match this profile."""

    response_with_no_condition = """- Age: 50
    - Gender: Female
    - Location: Los Angeles, CA
    - Debug Grid: [(34.0522, -118.2437)]
    
    I will now search for trials that match this profile."""

    # Validate the responses
    validation_result_1 = validate_medical_condition(response_with_common_condition)
    validation_result_2 = validate_medical_condition(response_with_uncommon_condition)
    validation_result_3 = validate_medical_condition(response_with_no_condition)

    print(f"Validation result for common condition: {validation_result_1}")
    print(f"Validation result for uncommon condition: {validation_result_2}")
    print(f"Validation result for no condition: {validation_result_3}")

if __name__ == "__main__":
    main()

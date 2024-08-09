# ./assistants/medical/response_validator.py
from validator_utils import validate_medical_condition, is_complete_response

def main():
    response_with_common_condition = '- Age: 50\n    - Gender: Female\n    - Medical Condition: Common Cold\n    - Location: Los Angeles, CA\n    - Debug Grid: [(34.0522, -118.2437)]\n    \n    I will now search for trials that match this profile.'
    response_with_uncommon_condition = '- Age: 50\n    - Gender: Female\n    - Medical Condition: Rare Disease\n    - Location: Los Angeles, CA\n    - Debug Grid: [(34.0522, -118.2437)]\n    \n    I will now search for trials that match this profile.'
    response_with_no_condition = '- Age: 50\n    - Gender: Female\n    - Location: Los Angeles, CA\n    - Debug Grid: [(34.0522, -118.2437)]\n    \n    I will now search for trials that match this profile.'
    validation_result_1 = validate_medical_condition(response_with_common_condition)
    validation_result_2 = validate_medical_condition(response_with_uncommon_condition)
    validation_result_3 = validate_medical_condition(response_with_no_condition)
    print(f'Validation result for common condition: {validation_result_1}')
    print(f'Validation result for uncommon condition: {validation_result_2}')
    print(f'Validation result for no condition: {validation_result_3}')
if __name__ == '__main__':
    main()

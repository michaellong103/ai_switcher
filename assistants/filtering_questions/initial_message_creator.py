import os
import json

def load_config_state():
    """
    Loads the config_state.json file from two directories up.

    Returns:
        dict: The content of the config_state.json file as a dictionary.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_state_path = os.path.join(current_dir, '..', '..', 'config_state.json')

    try:
        with open(config_state_path, 'r') as f:
            config_state = json.load(f)
        print(f'Successfully loaded JSON from {config_state_path}')
        return config_state
    except FileNotFoundError:
        print(f'Error: File not found: {config_state_path}')
    except json.JSONDecodeError:
        print(f'Error: JSON decoding failed for file: {config_state_path}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
    
    return {}

def create_initial_message():
    """
    Creates the initial message to be used by the system based on the config_state.json content.

    Returns:
        str: The initial message for the assistant.
    """
    config_state = load_config_state()

    # Extract relevant data from config_state
    api_params = config_state.get('current_api_params', {})
    stats = config_state.get('stats', {})

    number_of_trials = stats.get('number_of_trials', 'Unknown')
    medical_condition = api_params.get('Medical Condition', 'Unknown Condition')
    location = api_params.get('Location', 'Unknown Location')

    # Default message if the necessary data isn't present
    if number_of_trials == 'Unknown' or medical_condition == 'Unknown Condition' or location == 'Unknown Location':
        return "We couldn't retrieve all the necessary information to build a custom message. Please check the config state."

    # Construct the initial message
    initial_message = (
        f"Found {number_of_trials} Trials for {medical_condition} "
        f"within 203 Miles of {location}—Let’s Narrow the Results with a few questions."
    )

    return initial_message

if __name__ == "__main__":
    print(create_initial_message())

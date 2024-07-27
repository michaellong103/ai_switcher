# ./assistants/medical/medical_assistant.py
import logging
import os
import json
from colorama import Fore
from assistants.concrete_assistant import ConcreteAssistant
from assistants.create_dynamic_assistant import create_dynamic_assistant
from .medical_assistant_actions import MedicalAssistantActions
from .system_message import system_message
from .details_extractor import extract_details
from .validator_utils import validate_medical_condition, is_complete_response

class MedicalAssistant(ConcreteAssistant):
    def __init__(self, model='gpt-3.5-turbo', temperature=1, top_p=1):
        self.initial_message = "We need to sort through some questions to determine your eligibility for clinical trials. I will need age, condition, gender/sex, and location"
        super().__init__(system_message, model, temperature, top_p)

    def get_initial_message(self):
        return self.initial_message

    def get_response(self, user_input):
        if user_input.lower() == "switch_to_lunch":
            return "switch_to_lunch"
        
        actions = MedicalAssistantActions()
        action_response = actions.handle_actions(user_input)
        if action_response:
            return self.modify_response(action_response)
        response = super().get_response(user_input)
        return self.modify_response(response)

    def modify_response(self, response):
        if "Does this look correct? (y/n)" in response:
            print("Validating Assistant Output")
            logging.info("Validating Assistant Output")

        if "I will now search for trials that match this profile." in response:
            logging.info("Validating Assistant Output")

            if not is_complete_response(response):
                logging.warning("Incomplete response received")
                print(f"{Fore.RED}The response is incomplete or invalid. Please provide the necessary details again.{Fore.RESET}")
                return response  # Early return if the response is incomplete
            
            medical_condition_status = validate_medical_condition(response)
            print(f"{Fore.MAGENTA}Validation result: {medical_condition_status}{Fore.RESET}")
            
            if medical_condition_status:
                if medical_condition_status == "The data will be submitted with this criteria to find applicable trials.":
                    details = extract_details(response)
                    if details:
                        logging.info("User details collected successfully")

                        # Ensure the directory exists
                        os.makedirs('API_actions', exist_ok=True)

                        # Define the file path
                        file_path = 'API_actions/input.json'

                        # Delete the file if it exists
                        if os.path.exists(file_path):
                            os.remove(file_path)

                        # Create details.json with the content from extracted_details
                        with open(file_path, 'w') as json_file:
                            json.dump(details, json_file, indent=4)

                        response += f"\nYep, correct. Here is the response:\n{response}"
                        return response  # Return the modified response
                else:
                    response = self.get_response(medical_condition_status)
                    print(f"{Fore.BLUE}Assistant: {Fore.RESET}{response}")
                    return response

        return response

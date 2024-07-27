import logging
import os
import json
import asyncio
from colorama import Fore
from assistants.concrete_assistant import ConcreteAssistant
from assistants.create_dynamic_assistant import create_dynamic_assistant
from .medical_assistant_actions import MedicalAssistantActions
from .system_message import system_message
from .details_extractor import extract_details
from .validator_utils import validate_medical_condition, is_complete_response
from .async_caller import call_async_caller  # Import the function from the new file

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

                        # Define the file paths
                        input_file_path = 'API_actions/input.json'
                        output_file_path = 'API_response/output_final_big.json'

                        # Delete the input file if it exists
                        if os.path.exists(input_file_path):
                            os.remove(input_file_path)

                        # Write details to input.json
                        with open(input_file_path, 'w') as json_file:
                            json.dump(details, json_file, indent=4)

                        # Run async_caller_program.py using call_async_caller
                        try:
                            result_code, result_output = asyncio.run(call_async_caller(input_file_path, output_file_path))
                            logging.info(f"Script output: {result_output}")
                            response += f"\nScript ran successfully. Output:\n{result_output}"
                        except Exception as e:
                            logging.error(f"Error running async_caller_program: {e}")
                            response += f"\nError running async_caller_program: {e}"

                        return response  # Return the modified response
                else:
                    response = self.get_response(medical_condition_status)
                    print(f"{Fore.BLUE}Assistant: {Fore.RESET}{response}")
                    return response

        return response

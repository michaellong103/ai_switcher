# ./assistants/medical/medical_assistant.py

import logging
import os
import json
import subprocess
from colorama import Fore
from assistants.concrete_assistant import ConcreteAssistant
from assistants.create_dynamic_assistant import create_dynamic_assistant
from .medical_assistant_actions import MedicalAssistantActions
from .system_message import system_message
from .details_extractor import extract_details
from .validator_utils import validate_medical_condition, is_complete_response

class MedicalAssistant(ConcreteAssistant):
    def __init__(self, model='gpt-3.5-turbo', temperature=1, top_p=1):
        logging.info("Initializing MedicalAssistant with model: %s, temperature: %f, top_p: %f", model, temperature, top_p)
        self.initial_message = "We need to sort through some questions to determine your eligibility for clinical trials. I will need age, condition, gender/sex, and location"
        super().__init__(system_message, model, temperature, top_p)
        logging.info("MedicalAssistant initialized with initial_message: %s", self.initial_message)

    def get_initial_message(self):
        logging.info("get_initial_message called")
        return self.initial_message

    def respond(self, user_input):
        logging.info("respond called with user_input: %s", user_input)
        if user_input.lower() == "switch_to_lunch":
            logging.info("Switch to LunchAssistant requested")
            return "switch_to_lunch"
        actions = MedicalAssistantActions()
        action_response = actions.handle_actions(user_input)
        logging.info("Action response: %s", action_response)
        if action_response:
            modified_response = self.modify_response(action_response)
            logging.info("Modified action response: %s", modified_response)
            return modified_response
        response = super().get_response(user_input)
        modified_response = self.modify_response(response)
        logging.info("Modified super response: %s", modified_response)
        return modified_response

    def call_subprocess(self, script_path, *args):
        # Run a subprocess and capture its output
        process = subprocess.run(
            ['python', script_path, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if process.returncode == 0:
            logging.info(f"{os.path.basename(script_path)} completed successfully.")
        else:
            logging.error(f"{os.path.basename(script_path)} failed with return code {process.returncode}.")

        if process.stderr:
            logging.error(f"Script Errors:\n {process.stderr}")

        return process.returncode, process.stdout

    def call_sync_caller(self, input_file, output_file):
        # Resolve the path to async_caller_program.py
        caller_script = os.path.abspath(os.path.join('API_actions', 'async_caller_program.py'))
        return self.call_subprocess(caller_script, input_file, output_file)
    
    def run_query_stats(self):
        # Resolve the path to query_stats.py
        query_stats_script = os.path.abspath(os.path.join('tools', 'query_stats.py'))
        return self.call_subprocess(query_stats_script)

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

                        # Run sync_caller_program.py using call_sync_caller
                        try:
                            result_code, result_output = self.call_sync_caller(input_file_path, output_file_path)
                      
                        except Exception as e:
                            logging.error(f"Error running sync_caller_program: {e}")
                            response += f"\nError running sync_caller_program: {e}"

                        return response  # Return the modified response
                else:
                    response = self.get_response(medical_condition_status)
                    print(f"{Fore.BLUE}Assistant: {Fore.RESET}{response}")
                    return response

        return response

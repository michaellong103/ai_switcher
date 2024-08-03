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
from API_actions.async_caller_program import call_api_query
from tools.query_stats import count_trials

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

    def execute_api_query(self, input_file, output_file):
        # Log the function call with input parameters
        logging.info(f"Executing API query with input_file: {input_file}, output_file: {output_file}")

        # Directly call the synchronous function
        return_code, api_response = call_api_query(input_file, output_file)

        if return_code == 0:
            logging.info("The API query is complete, and the files have been written successfully.")
            return return_code, api_response
        else:
            logging.error("There was an issue with the API query.")
            return return_code, api_response

    def run_query_stats(self):
        try:
            logging.info("Running query_stats directly")
            # Directly call the function to count trials
            stats_summary = count_trials()

            if stats_summary:
                logging.info("query_stats completed successfully.")
                return 0, stats_summary
            else:
                logging.error("query_stats failed with errors.")
                return 1, "Failed to complete query stats"

        except Exception as e:
            logging.error(f"Exception occurred while running query_stats: {e}")
            return 1, str(e)

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

                        # Run API query using execute_api_query
                        try:
                            result_code, result_output = self.execute_api_query(input_file_path, output_file_path)

                        except Exception as e:
                            logging.error(f"Error executing API query: {e}")
                            response += f"\nError executing API query: {e}"

                        return response  # Return the modified response
                else:
                    response = self.get_response(medical_condition_status)
                    print(f"{Fore.BLUE}Assistant: {Fore.RESET}{response}")
                    return response

        return response

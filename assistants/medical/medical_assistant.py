# ./assistants/medical/medical_assistant.py
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

    async def call_async_caller(self, input_file, output_file):
        # Resolve the path to async_caller_program.py
        async_caller_script = os.path.abspath(os.path.join('API_actions', 'async_caller_program.py'))

        process = await asyncio.create_subprocess_exec(
            'python', async_caller_script, input_file, output_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Wait for the process to complete and capture output
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            logging.info("async_caller_program.py completed successfully.")
        else:
            logging.error(f"async_caller_program.py failed with return code {process.returncode}.")

        if stderr:
            logging.error(f"Script Errors:\n {stderr.decode()}")

        return process.returncode, stdout.decode()
    
    async def run_query_stats(self):
        # Resolve the path to query_stats.py
        query_stats_script = os.path.abspath(os.path.join('tools', 'query_stats.py'))

        process = await asyncio.create_subprocess_exec(
            'python', query_stats_script,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Wait for the process to complete and capture output
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            logging.info("query_stats.py completed successfully.")
        else:
            logging.error(f"query_stats.py failed with return code {process.returncode}.")

        if stderr:
            logging.error(f"Script Errors:\n {stderr.decode()}")

        return process.returncode, stdout.decode()

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
                            result_code, result_output = asyncio.run(self.call_async_caller(input_file_path, output_file_path))
                            logging.info(f"Script output: {result_output}")
                            response += f"\nScript ran successfully. Output:\n{result_output}"
                            result_code, result_output = asyncio.run(self.run_query_stats())
                            logging.info(f"query_stats.py output: {result_output}")
                            response += f"\nquery_stats.py ran successfully. Output:\n{result_output}"
                      
                        except Exception as e:
                            logging.error(f"Error running async_caller_program: {e}")
                            response += f"\nError running async_caller_program: {e}"

                        return response  # Return the modified response
                else:
                    response = self.get_response(medical_condition_status)
                    print(f"{Fore.BLUE}Assistant: {Fore.RESET}{response}")
                    return response

        return response

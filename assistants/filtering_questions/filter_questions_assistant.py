import time
import logging
from assistants.concrete_assistant import ConcreteAssistant
from .build_system_message import build_system_message_file
from .filter_questions_assistant_actions import FilterQuestionsAssistantActions  # Import the actions class

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

build_system_message_file()

time.sleep(0.1)  # 100 milliseconds

from .system_message import system_message, initial_message

class FilterQuestionsAssistant(ConcreteAssistant):

    def __init__(self, model='gpt-3.5-turbo', temperature=0.7, top_p=0.9):
        logging.info(f'Initializing FilterQuestionsAssistant with model: {model}, temperature: {temperature}, top_p: {top_p}')
        super().__init__(system_message, model, temperature, top_p)
        self.actions = FilterQuestionsAssistantActions()  # Initialize the actions class
        logging.info(f'FilterQuestionsAssistant initialized with initial_message: {initial_message}')

    def get_initial_message(self):
        logging.info('get_initial_message called')
        return initial_message

    def respond(self, user_input):
        logging.info(f'respond called with user_input: {user_input}')
        
        # Handle actions
        action_response = self.actions.handle_actions(user_input)
        if action_response:
            logging.info(f'Action response: {action_response}')
            return action_response

        # Fallback to regular response
        response = super().get_response(user_input)

        # Modify response to detect (y/n) or (Y/N)
        response = self.modify_response(response)
        logging.info(f'FilterQuestionsAssistant response after modification: {response}')
        
        return response

    def modify_response(self, response):
        """
        Modify the response if it contains 'Confirmed' and any of the following words:
        'duration', 'years', 'months', 'days', 'time'.
        Additionally, log 'Found Confirmed' if both conditions are met.
        """
        logging.info(f'modify_response called with response: {response}')

        # Define the keywords to check
        keywords = ["duration", "years", "months", "days", "time"]

        # Check if 'Confirmed' is in the response and if any keyword is present
        if "Confirmed" in response and any(word in response for word in keywords):
            # Log "Found Confirmed" if the conditions are met
            print('Found Confirmed 88888888')
            
            # Avoid duplicating the modification
            if "Please provide more details regarding the timeframe." not in response:
                # Modify the response as needed
                modified_response = response + " - Please provide more details regarding the timeframe."
                logging.info(f'Response modified to: {modified_response}')
                return modified_response

        # Return the original response if no modifications are needed
        return response

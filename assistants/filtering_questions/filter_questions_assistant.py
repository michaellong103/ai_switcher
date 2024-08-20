# ./filter_questions_assistant.py
import logging
import time
from assistants.concrete_assistant import ConcreteAssistant
from .build_system_message import build_system_message_file
from .filter_questions_assistant_actions import FilterQuestionsAssistantActions  # Import the actions class

build_system_message_file()

time.sleep(0.1)  # 100 milliseconds

from .system_message import system_message, initial_message

class FilterQuestionsAssistant(ConcreteAssistant):

    def __init__(self, model='gpt-3.5-turbo', temperature=0.7, top_p=0.9):
        logging.info('Initializing FilterQuestionsAssistant with model: %s, temperature: %f, top_p: %f', model, temperature, top_p)
        super().__init__(system_message, model, temperature, top_p)
        self.actions = FilterQuestionsAssistantActions()  # Initialize the actions class
        logging.info('FilterQuestionsAssistant initialized with initial_message: %s', initial_message)

    def get_initial_message(self):
        logging.info('get_initial_message called')
        return initial_message

    def respond(self, user_input):
        logging.info('respond called with user_input: %s', user_input)
        
        # Handle actions
        action_response = self.actions.handle_actions(user_input)
        if action_response:
            logging.info('Action response: %s', action_response)
            return action_response

        # Fallback to regular response
        response = super().get_response(user_input)
        logging.info('FilterQuestionsAssistant response: %s', response)
        return response

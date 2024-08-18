# ./assistants/filtering_questions/filter_questions_assistant.py

import logging
from assistants.concrete_assistant import ConcreteAssistant
from .system_message import system_message

class FilterQuestionsAssistant(ConcreteAssistant):

    def __init__(self, model='gpt-3.5-turbo', temperature=0.7, top_p=0.9):
        logging.info('Initializing FilterQuestionsAssistant with model: %s, temperature: %f, top_p: %f', model, temperature, top_p)
        self.initial_message = "I'm here to help filter and categorize your questions. Please ask your question, and I'll do my best to classify it."
        super().__init__(system_message, model, temperature, top_p)
        logging.info('FilterQuestionsAssistant initialized with initial_message: %s', self.initial_message)

    def get_initial_message(self):
        logging.info('get_initial_message called')
        return self.initial_message

    def respond(self, user_input):
        logging.info('respond called with user_input: %s', user_input)
        response = super().get_response(user_input)
        logging.info('FilterQuestionsAssistant response: %s', response)
        return response

# ./assistants/lunch/lunch_assistant.py

import logging
from assistants.concrete_assistant import ConcreteAssistant

class LunchAssistant(ConcreteAssistant):
    def __init__(self, model='gpt-3.5-turbo', temperature=1, top_p=1):
        logging.info("Initializing LunchAssistant")
        system_message = {
            "role": "system",
            "content": (
                "You are a friendly assistant helping users decide on what to have for lunch.\n\n"
                "Requirements:\n\n"
                "- Suggest a variety of cuisines.\n"
                "- Ask about dietary restrictions.\n"
                "- Provide healthy options.\n"
                "- Offer suggestions based on time of day.\n"
                "- Be polite and engaging."
            )
        }
        self.initial_message = "Hello! I'm here to help you decide what to have for lunch. Do you have any dietary restrictions?"
        logging.info(f"LunchAssistant system_message: {system_message}")
        super().__init__(system_message, model, temperature, top_p)

    def get_initial_message(self):
        logging.info("get_initial_message called")
        return self.initial_message

    def respond(self, user_input):
        logging.info(f"LunchAssistant respond called with user_input: {user_input}")
        if user_input.lower() == "switch_to_medical":
            logging.info("Switching to MedicalAssistant requested")
            return "switch_to_medical"
        response = self.get_response(user_input)
        logging.info(f"LunchAssistant response: {response}")
        return response

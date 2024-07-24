# ./router/conversation_router.py

from assistants.lunch.lunch_assistant import LunchAssistant  # Ensure lunch assistant path is correct
from assistants.medical.medical_assistant import MedicalAssistant  # Corrected import path
from assistants.concrete_assistant import ConcreteAssistant

class ConversationRouter:
    def __init__(self, assistants):
        self.assistants = assistants
        self.current_assistant = assistants[0]

    def route(self, message):
        response = self.current_assistant.respond(message)
        if response == "switch_to_lunch":
            self.switch_to_lunch_assistant()
            response = "Assistant switched to Lunch Assistant for lunch recommendations."
        elif response == "switch_to_dynamic":
            self.switch_to_dynamic_assistant()
            response = "Let's talk about trials that might suit you."
        if response is None:
            response = "No response from the assistant."
        return response

    def switch_to_lunch_assistant(self):
        for assistant in self.assistants:
            if isinstance(assistant, LunchAssistant):
                self.current_assistant = assistant
                break

    def switch_to_dynamic_assistant(self):
        for assistant in self.assistants:
            if isinstance(assistant, MedicalAssistant):
                dynamic_assistant = assistant.create_and_switch_to_dynamic_assistant()
                if isinstance(dynamic_assistant, ConcreteAssistant):
                    self.current_assistant = dynamic_assistant
                    break
                else:
                    print(dynamic_assistant)  # Prints the error message if dynamic assistant creation fails

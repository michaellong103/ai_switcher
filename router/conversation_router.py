# ./router/conversation_router.py

from assistants.testing_assistant import TestingAssistant  # Import TestingAssistant

class ConversationRouter:
    def __init__(self, assistants):
        self.assistants = assistants
        self.current_assistant = assistants[0]

    def route(self, message):
        response = self.current_assistant.respond(message)
        if response == "switch_to_lunch":
            self.switch_to_testing_assistant()
            response = "Assistant switched to Testing Assistant for lunch recommendations."
        if response is None:
            response = "No response from the assistant."
        return response

    def switch_to_testing_assistant(self):
        for assistant in self.assistants:
            if isinstance(assistant, TestingAssistant):
                self.current_assistant = assistant
                break

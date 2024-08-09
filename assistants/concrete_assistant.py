# ./assistants/concrete_assistant.py
from .base_assistant import BaseAssistant

class ConcreteAssistant(BaseAssistant):

    def respond(self, user_input):
        return self.get_response(user_input)

# ./assistants/testing_assistant.py

from .concrete_assistant import ConcreteAssistant

class TestingAssistant(ConcreteAssistant):
    def __init__(self, model='gpt-3.5-turbo', temperature=1, top_p=1):
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
        super().__init__(system_message, model, temperature, top_p)

    def get_initial_message(self):
        return self.initial_message

# ./tests/test_router.py
import unittest
from router.conversation_router import ConversationRouter
from assistants.medical_assistant import MedicalAssistant
from assistants.testing_assistant import TestingAssistant
from assistants.dynamic_assistant import create_dynamic_assistant

class MockAssistant:
    def __init__(self, name, response):
        self.name = name
        self.response = response

    def respond(self, message):
        if message == "I need lunch":
            return "switch_to_lunch"
        return self.response

class TestConversationRouter(unittest.TestCase):
    def setUp(self):
        # Create mock assistants
        self.medical_assistant = MockAssistant("MedicalAssistant", "Medical response")
        self.testing_assistant = MockAssistant("TestingAssistant", "Testing response")

        # Create router with mock assistants
        self.router = ConversationRouter([self.medical_assistant, self.testing_assistant])

    def test_initial_routing(self):
        response = self.router.route("Hello")
        self.assertEqual(response, "Medical response")

    def test_switching_assistants(self):
        response = self.router.route("I need lunch")
        self.assertEqual(response, "Assistant switched to Testing Assistant for lunch recommendations.")
        response = self.router.route("Hello")
        self.assertEqual(response, "Testing response")

    def test_no_response(self):
        self.medical_assistant.response = None
        response = self.router.route("Hello")
        self.assertEqual(response, "No response from the assistant.")

    def test_dynamic_assistant(self):
        config = {
            "system_message": "You are a dynamic assistant.",
            "initial_message": "Hello! How can I assist you?"
        }
        DynamicAssistant = create_dynamic_assistant(config)
        dynamic_assistant = DynamicAssistant()
        self.router = ConversationRouter([self.medical_assistant, dynamic_assistant])
        
        initial_message = dynamic_assistant.get_initial_message()
        self.assertEqual(initial_message, config['initial_message'])
        
        response = dynamic_assistant.get_response("Hello")
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()

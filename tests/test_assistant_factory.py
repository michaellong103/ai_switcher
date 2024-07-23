# ./tests/test_assistant_factory.py
import unittest
from assistants.assistant_factory import create_assistant

class TestAssistantFactory(unittest.TestCase):
    def test_create_medical_assistant(self):
        assistant = create_assistant(assistant_type="medical")
        self.assertEqual(assistant.__class__.__name__, "MedicalAssistant")

    def test_create_testing_assistant(self):
        assistant = create_assistant(assistant_type="testing")
        self.assertEqual(assistant.__class__.__name__, "TestingAssistant")

    def test_create_dynamic_assistant(self):
        config = {
            "system_message": "You are a dynamic assistant.",
            "initial_message": "Hello! How can I assist you?"
        }
        DynamicAssistant = create_assistant(assistant_type="dynamic", config=config)
        self.assertEqual(DynamicAssistant.__class__.__name__, "DynamicAssistant")
        self.assertEqual(DynamicAssistant().get_initial_message(), config['initial_message'])

if __name__ == '__main__':
    unittest.main()

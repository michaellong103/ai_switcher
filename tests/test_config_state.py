# File: ./tests/test_config_state.py

import unittest
import json
import os
from assistants.medical.medical_assistant import MedicalAssistant  # Adjust import as needed

class TestConfigState(unittest.TestCase):
    
    def setUp(self):
        # Path to config_state.json
        self.config_state_path = os.path.join(os.path.dirname(__file__), '..', 'config_state.json')

        # Initialize the MedicalAssistant
        self.assistant = MedicalAssistant()

        # Ensure config_state.json starts with a clean state
        initial_state = {
            "current_api_params": {}
        }
        with open(self.config_state_path, 'w') as file:
            json.dump(initial_state, file, indent=4)

    def simulate_conversation(self, assistant, user_input_sequence):
        """
        Simulates a conversation with the assistant using the given input sequence.
        """
        for user_input in user_input_sequence:
            response = assistant.respond(user_input)
            print(response)  # Optionally print responses for debugging purposes

    def test_config_state_update(self):
        """
        Test to ensure the config_state.json is updated correctly after conversation.
        """
        # Simulate the conversation
        user_input_sequence = [
            "50 female breast cancer triple negative Los Angeles",
            "y"  # Confirmation
        ]

        # Execute the conversation
        self.simulate_conversation(self.assistant, user_input_sequence)

        # Read the config_state.json file
        with open(self.config_state_path, 'r') as file:
            state_data = json.load(file)

        # Expected API params
        expected_params = {
            "Age": "50",
            "Gender": "Female",
            "Medical Condition": "Triple Negative Breast Cancer",
            "Location": "Los Angeles, CA",
            "Latitude": "34.0522",
            "Longitude": "-118.2437"
        }

        # Assert that the current_api_params match the expected values
        self.assertEqual(state_data["current_api_params"], expected_params)

    def tearDown(self):
        # Clean up by resetting the config_state.json file if necessary
        if os.path.exists(self.config_state_path):
            os.remove(self.config_state_path)

if __name__ == '__main__':
    unittest.main()

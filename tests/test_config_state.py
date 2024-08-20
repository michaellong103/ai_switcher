# ./tests/test_config_state.py
import unittest
import json
import os
from assistants.medical.medical_assistant import MedicalAssistant

class TestConfigState(unittest.TestCase):

    def setUp(self):
        self.config_state_path = os.path.join(os.path.dirname(__file__), '..', 'config_state.json')
        self.assistant = MedicalAssistant()
        initial_state = {'current_api_params': {}}
        with open(self.config_state_path, 'w') as file:
            json.dump(initial_state, file, indent=4)

    def simulate_conversation(self, assistant, user_input_sequence):
        for user_input in user_input_sequence:
            response = assistant.respond(user_input)
            print(response)

    def test_config_state_update(self):
        user_input_sequence = ['50 female breast cancer triple negative Los Angeles', 'y']
        self.simulate_conversation(self.assistant, user_input_sequence)
        with open(self.config_state_path, 'r') as file:
            state_data = json.load(file)
        expected_params = {'Age': '50', 'Gender': 'Female', 'Medical Condition': 'Triple Negative Breast Cancer', 'Location': 'Los Angeles, CA', 'Latitude': '34.0522', 'Longitude': '-118.2437'}
        self.assertEqual(state_data['current_api_params'], expected_params)

    def tearDown(self):
        if os.path.exists(self.config_state_path):
            os.remove(self.config_state_path)
if __name__ == '__main__':
    unittest.main()

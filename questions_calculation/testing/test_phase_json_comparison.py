# ./questions_calculation/testing/test_phase_json_comparison.py

import unittest
import json
import os

class TestPhaseJSONComparison(unittest.TestCase):

    def setUp(self):
        # Paths to JSON files
        final_json_path = os.path.join(os.path.dirname(__file__), '../final_question_output.json')
        phase_json_path = os.path.join(os.path.dirname(__file__), '../../API_response/phase_question_output.json')
        
        # Load the JSON files
        with open(final_json_path, 'r') as final_file:
            self.final_data = json.load(final_file)
        
        with open(phase_json_path, 'r') as phase_file:
            self.phase_data = json.load(phase_file)
    
    def test_phase_data_in_final(self):
        # Ensure all NCT numbers from phase_question_output.json are in final_question_output.json, with phase information.
        print("\n\033[94m--- Starting Phase NCT Number Subset Comparison ---\033[0m")
        
        # Extract relevant data from final_question_output.json
        final_question = self.final_data['qs'][1]  # The second question relates to phase_question_output.json
        final_groups = final_question['data']['opts']

        # Walk through phase_question_output.json and ensure its data is in final_question_output.json
        for phase_option in self.phase_data.get('options', []):
            phase_nct_numbers = set(phase_option.get('NCTNumbers', []))
            phase_text = phase_option.get('optionText', 'Unknown Phase')
            matching_group = next((grp for grp in final_groups if grp['NCTc'] == phase_option['NCTCount']), None)
            
            print(f"\n\033[94mComparing group with NCT count {phase_option['NCTCount']} for phase '{phase_text}'...\033[0m")
            
            # Assert that each group from phase_question_output.json is present in final_question_output.json
            self.assertIsNotNone(
                matching_group, 
                f"\033[91mGroup with NCT count {phase_option['NCTCount']} and phase '{phase_text}' not found in final output.\033[0m"
            )
            print(f"\033[92mGroup with NCT count {phase_option['NCTCount']} for phase '{phase_text}' found.\033[0m")
            
            # Assert that all NCT numbers in phase_option are present in the final output group
            final_nct_numbers = set(matching_group.get('NCTn', []))
            missing_ncts = phase_nct_numbers - final_nct_numbers
            
            if not missing_ncts:
                print(f"\033[92mAll NCT numbers from phase '{phase_text}' are present in the final group with NCT count {phase_option['NCTCount']}\033[0m")
            else:
                print(f"\033[91mNCT numbers missing in final output for group with NCT count {phase_option['NCTCount']} and phase '{phase_text}':\033[0m {missing_ncts}")
            
            self.assertTrue(
                missing_ncts == set(), 
                f"\033[91mSome NCT numbers from phase_question_output.json are missing in final_question_output.json for group with NCT count {phase_option['NCTCount']} and phase '{phase_text}'\033[0m"
            )

if __name__ == '__main__':
    unittest.main()

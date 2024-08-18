# ./testing/test_json_comparison.py

import unittest
import json
import os

class TestJSONComparison(unittest.TestCase):

    def setUp(self):
        # Paths to JSON files
        final_json_path = os.path.join(os.path.dirname(__file__), '../final_question_output.json')
        times_json_path = os.path.join(os.path.dirname(__file__), '../../API_response/times_question_output.json')
        
        # Load the JSON files
        with open(final_json_path, 'r') as final_file:
            self.final_data = json.load(final_file)
        
        with open(times_json_path, 'r') as times_file:
            self.times_data = json.load(times_file)
    
    def test_group_mapping(self):
        """Ensure all groups from times_question_output.json map to a group with 'term' in the name in final_question_output.json."""
        print("\n\033[94m--- Starting Group Mapping Verification ---\033[0m")
        
        # Extract relevant data from final_question_output.json
        final_question = self.final_data['qs'][0]  # The first question relates to times_question_output.json
        final_groups = final_question['data']

        # Expected mapping of original group names to "term" groups in the final file
        term_keywords = ['term']

        # Walk through times_question_output.json and verify mappings
        for times_group in self.times_data:
            times_group_name = times_group.get('trialGroup', 'Unnamed Group')
            times_total = times_group['total']
            matching_group = next((grp for grp in final_groups if grp['tot'] == times_total), None)
            
            print(f"\n\033[94mChecking mapping for {times_group_name} (Total trials: {times_total})...\033[0m")
            
            # Check if the group exists in the final output
            self.assertIsNotNone(
                matching_group, 
                f"\033[91mGroup '{times_group_name}' with total {times_total} not found in final output.\033[0m"
            )
            print(f"\033[92mGroup '{times_group_name}' found in final output.\033[0m")
            
            # Verify that the final group name contains the word 'term'
            final_group_name = matching_group.get('grp', 'Unnamed Group')
            if not any(keyword in final_group_name.lower() for keyword in term_keywords):
                self.fail(f"\033[91mGroup '{times_group_name}' (Total trials: {times_total}) was incorrectly mapped to '{final_group_name}', which does not contain the word 'term'.\033[0m")
            else:
                print(f"\033[92mGroup '{times_group_name}' correctly mapped to '{final_group_name}'.\033[0m")
    
    def test_group_fields_match(self):
        """Ensure that key fields within matching groups are consistent."""
        print("\n\033[94m--- Starting Group Field Comparison ---\033[0m")
        
        final_question = self.final_data['qs'][0]
        final_groups = final_question['data']

        for times_group in self.times_data:
            times_total = times_group['total']
            matching_group = next((grp for grp in final_groups if grp['tot'] == times_total), None)
            
            print(f"\n\033[94mComparing group labels for group with total {times_total} trials...\033[0m")
            
            # Check that a matching group exists
            self.assertIsNotNone(
                matching_group, 
                f"\033[91mGroup with total {times_total} not found in final output.\033[0m"
            )
            print(f"\033[92mMatching group found for total {times_total}.\033[0m")

            # Compare additional fields like trialGroup, dateSpan, etc.
            expected_label = self.get_expected_label(times_group.get('trialGroup'))
            print(f"\033[94mExpected label: {expected_label}\033[0m")
            print(f"\033[94mFinal label: {matching_group.get('grp')}\033[0m")
            
            self.assertEqual(
                expected_label, 
                matching_group.get('grp'), 
                f"\033[91mGroup label mismatch for group with total {times_total}.\033[0m"
            )
            print(f"\033[92mGroup labels match for group with total {times_total}.\033[0m")

    def get_expected_label(self, original_label):
        """Helper function to map original labels to expected labels."""
        label_mapping = {
            'Group 1': 'Short-term (120-742 days, approximately 4 months to 2 years)',
            'Group 2': 'Medium-term (774-1201 days, approximately 2 to 3.5 years)',
            'Group 3': 'Long-term (1231-3209 days, approximately 3.5 to 9 years)'
        }
        return label_mapping.get(original_label, original_label)

if __name__ == '__main__':
    unittest.main()

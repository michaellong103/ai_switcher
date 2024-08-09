import os
import json
import unittest
from evaluate_trials import load_config, load_trials_data, evaluate_number_of_trials

class TestEvaluateTrials(unittest.TestCase):

    def setUp(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.script_dir, 'test_config.json')
        self.trials_path = os.path.join(self.script_dir, 'test_finaloutput.json')
        self.config_data = {'no_trials': 0, 'few_trials': 1, 'a_lot_of_trials': 6, 'too_many_trials': 14}
        with open(self.config_path, 'w') as f:
            json.dump(self.config_data, f, indent=4)
        self.trials_data = {'studies': [{'studyName': 'Study 1', 'nctNumber': 'NCT000001'}, {'studyName': 'Study 2', 'nctNumber': 'NCT000002'}, {'studyName': 'Study 3', 'nctNumber': 'NCT000003'}, {'studyName': 'Study 4', 'nctNumber': 'NCT000004'}, {'studyName': 'Study 5', 'nctNumber': 'NCT000005'}, {'studyName': 'Study 6', 'nctNumber': 'NCT000006'}, {'studyName': 'Study 7', 'nctNumber': 'NCT000007'}, {'studyName': 'Study 8', 'nctNumber': 'NCT000008'}, {'studyName': 'Study 9', 'nctNumber': 'NCT000009'}]}
        with open(self.trials_path, 'w') as f:
            json.dump(self.trials_data, f, indent=4)

    def test_load_config(self):
        config = load_config(self.config_path)
        self.assertEqual(config, self.config_data)

    def test_load_trials_data(self):
        trials = load_trials_data(self.trials_path)
        self.assertEqual(len(trials), 9)
        self.assertEqual(trials[0]['studyName'], 'Study 1')

    def test_evaluate_number_of_trials(self):
        config = self.config_data
        no_trials_response = evaluate_number_of_trials([], config)
        self.assertEqual(no_trials_response, 'No trials')
        few_trials_response = evaluate_number_of_trials(self.trials_data['studies'][:2], config)
        self.assertEqual(few_trials_response, 'Few trials')
        a_lot_of_trials_response = evaluate_number_of_trials(self.trials_data['studies'][:9], config)
        self.assertEqual(a_lot_of_trials_response, 'A lot of trials')
        too_many_trials_data = self.trials_data['studies'] * 2
        too_many_trials_response = evaluate_number_of_trials(too_many_trials_data, config)
        self.assertEqual(too_many_trials_response, 'Too many trials')

    def test_invalid_config_file(self):
        invalid_config_path = os.path.join(self.script_dir, 'invalid_test_config.json')
        with open(invalid_config_path, 'w') as f:
            f.write('{invalid_json}')
        with self.assertRaises(json.JSONDecodeError):
            load_config(invalid_config_path)
        os.remove(invalid_config_path)

    def test_missing_trials_field(self):
        trials_path_missing_field = os.path.join(self.script_dir, 'test_missing_field.json')
        invalid_trials_data = {'invalid_key': [{'studyName': 'Study 1', 'nctNumber': 'NCT000001'}]}
        with open(trials_path_missing_field, 'w') as f:
            json.dump(invalid_trials_data, f, indent=4)
        trials = load_trials_data(trials_path_missing_field)
        self.assertEqual(len(trials), 0)
        os.remove(trials_path_missing_field)

    def test_boundary_trials(self):
        config = self.config_data
        boundary_trials = self.trials_data['studies'][:5]
        boundary_trials_response = evaluate_number_of_trials(boundary_trials, config)
        self.assertEqual(boundary_trials_response, 'Few trials')
        boundary_trials = self.trials_data['studies'][:6]
        boundary_trials_response = evaluate_number_of_trials(boundary_trials, config)
        self.assertEqual(boundary_trials_response, 'A lot of trials')
        boundary_trials = self.trials_data['studies'] * 2
        boundary_trials_response = evaluate_number_of_trials(boundary_trials[:14], config)
        self.assertEqual(boundary_trials_response, 'Too many trials')

    def tearDown(self):
        os.remove(self.config_path)
        os.remove(self.trials_path)
if __name__ == '__main__':
    unittest.main(verbosity=2)

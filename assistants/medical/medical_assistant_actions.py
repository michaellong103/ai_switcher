# ./assistants/medical/medical_assistant_actions.py
class MedicalAssistantActions:

    def handle_actions(self, user_input):
        if user_input.lower() == 'i need lunch':
            return 'switch_to_lunch'
        return None

    def create_and_switch_to_dynamic_assistant(self):
        config_path = './assistants/as_configs/exclusion_AI.json'
        additional_data_path = './JSON/sort_debug_exclusion.json'
        try:
            dynamic_assistant = create_dynamic_assistant(config_path, additional_data_path)
            return dynamic_assistant
        except RuntimeError as e:
            return f'Failed to create dynamic assistant: {e}'

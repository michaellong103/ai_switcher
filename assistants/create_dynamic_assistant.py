# ./assistants/create_dynamic_assistant.py
import json
import requests
import logging
from .concrete_assistant import ConcreteAssistant

def create_dynamic_assistant(config_path, additional_data_path):
    try:
        logging.info(f'Attempting to open config file at: {config_path}')
        with open(config_path, 'r') as config_file:
            config_content = config_file.read()
            logging.info(f'Config file content: {config_content}')
            config = json.loads(config_content)
        logging.info(f'Attempting to open additional data file at: {additional_data_path}')
        with open(additional_data_path, 'r') as additional_data_file:
            additional_data_content = additional_data_file.read()
            logging.info(f'Additional data file content: {additional_data_content}')
            additional_data = json.loads(additional_data_content)
        logging.info(f'Additional data: {additional_data}')
        config['system_message']['content'] += f'\n\nAdditional Data:\n{json.dumps(additional_data, indent=2)}'
        dynamic_assistant = ConcreteAssistant(system_message=config['system_message'], model=config['model'], temperature=config['temperature'], top_p=config['top_p'])
        return dynamic_assistant
    except requests.exceptions.RequestException as e:
        logging.error(f'RequestException: {e}')
        raise RuntimeError(f'Failed to create dynamic assistant: {e}')
    except json.JSONDecodeError as e:
        logging.error(f'JSONDecodeError: {e}')
        raise RuntimeError(f'Failed to create dynamic assistant: {e}')
    except Exception as e:
        logging.error(f'Exception: {e}')
        raise RuntimeError(f'Failed to create dynamic assistant: {e}')

# ./assistants/assistant_factory.py
from .concrete_assistant import ConcreteAssistant
from .medical.medical_assistant import MedicalAssistant
from .lunch.lunch_assistant import LunchAssistant
import logging

def create_assistant(assistant_type='default', system_message=None, model='default-model', temperature=0.7, top_p=0.9):
    logging.info(f'Creating assistant with type: {assistant_type}')
    if not system_message:
        system_message = {'role': 'system', 'content': 'You are a helpful assistant.'}
    if assistant_type == 'medical':
        logging.info('Creating MedicalAssistant')
        return MedicalAssistant(model, temperature, top_p)
    elif assistant_type == 'lunch':
        logging.info('Creating LunchAssistant')
        return LunchAssistant()
    elif assistant_type == 'testing':
        logging.info('Creating TestingAssistant')
        return TestingAssistant(model, temperature, top_p)
    logging.info('Creating ConcreteAssistant')
    return ConcreteAssistant(system_message, model, temperature, top_p)

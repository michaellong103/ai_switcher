# ./router/conversation_router.py

import logging
from assistants.lunch.lunch_assistant import LunchAssistant
from assistants.medical.medical_assistant import MedicalAssistant
from assistants.concrete_assistant import ConcreteAssistant
import os
from API_actions.event_manager import EventManager

class TerminalMessagePrinter:
    def respond(self, message):
        return f"Terminal message: {message}"

class ConversationRouter:
    def __init__(self, assistants):
        self.assistants = assistants
        self.current_assistant = assistants[0]
        self.terminal_printer = TerminalMessagePrinter()
        logging.info(f"Initial assistant: {type(self.current_assistant).__name__}")
        self.notification_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'router_notification.txt'))

        # Create an instance of the EventManager
        self.event_manager = EventManager()

        # Register the router to listen for the 'no_trials_found' event
        self.event_manager.register('no_trials_found', self.switch_to_terminal_printer)

    def check_notifications(self):
        if os.path.exists(self.notification_file):
            with open(self.notification_file, 'r') as file:
                message = file.read()
            os.remove(self.notification_file)
            return message
        return None

    def route(self, message):
        notification_message = self.check_notifications()
        if notification_message:
            self.switch_to_terminal_printer()
            return self.current_assistant.respond(notification_message)

        response = self.current_assistant.respond(message)
        logging.info(f"Response from {type(self.current_assistant).__name__}: {response}")
        
        if response == "switch_to_lunch":
            self.switch_to_lunch_assistant()
            response = "Assistant switched to Lunch Assistant for lunch recommendations."
            logging.info(f"Assistant switched to: {type(self.current_assistant).__name__}")
        elif response == "switch_to_dynamic":
            self.switch_to_dynamic_assistant()
            response = "Let's talk about trials that might suit you."
            logging.info(f"Assistant switched to: {type(self.current_assistant).__name__}")
        elif response == "switch_to_terminal":
            self.switch_to_terminal_printer()
            response = "Switched to terminal message printer."
            logging.info("Switched to terminal message printer.")
        
        if response is None:
            response = "No response from the assistant."
        
        logging.info(f"Assistant response after routing: {response}")
        return response

    def switch_to_lunch_assistant(self):
        logging.info("Attempting to switch to Lunch Assistant")
        for assistant in self.assistants:
            logging.info(f"Checking assistant: {type(assistant).__name__}")
            if isinstance(assistant, LunchAssistant):
                logging.info("Switching to Lunch Assistant")
                self.current_assistant = assistant
                logging.info(f"Current assistant set to: {type(self.current_assistant).__name__}")
                return
        logging.error("Lunch Assistant not found. Switching failed.")
        logging.info(f"Current assistant after switch attempt: {type(self.current_assistant).__name__}")

    def switch_to_dynamic_assistant(self):
        logging.info("Attempting to switch to Dynamic Medical Assistant")
        for assistant in self.assistants:
            if isinstance(assistant, MedicalAssistant):
                logging.info("Found Medical Assistant. Creating dynamic assistant.")
                dynamic_assistant = assistant.create_and_switch_to_dynamic_assistant()
                if isinstance(dynamic_assistant, ConcreteAssistant):
                    self.current_assistant = dynamic_assistant
                    logging.info(f"Current assistant: {type(self.current_assistant).__name__}")
                    return
                else:
                    logging.error("Failed to create dynamic assistant")
        logging.error("Dynamic Medical Assistant not found. Switching failed.")

    def switch_to_terminal_printer(self, *args, **kwargs):
        logging.info("Switching to Terminal Message Printer")
        self.current_assistant = self.terminal_printer
        logging.info(f"Current assistant set to: {type(self.current_assistant).__name__}")


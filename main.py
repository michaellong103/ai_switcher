# ./main.py

import sys
import logging
import os
from colorama import Fore, Style, init
from assistants.assistant_factory import create_assistant
from router.conversation_router import ConversationRouter
from assistants.lunch.lunch_assistant import LunchAssistant
from assistants.medical.medical_assistant import MedicalAssistant
from assistants.concrete_assistant import ConcreteAssistant

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'assistants')))

init(autoreset=True)

log_directory = "logs"

def delete_logs():
    """Delete log files in the log directory."""
    if os.path.exists(log_directory):
        for log_file in os.listdir(log_directory):
            file_path = os.path.join(log_directory, log_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"Deleted log file: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

delete_logs()

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

class TruncateFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%', max_length=100):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.max_length = max_length

    def format(self, record):
        # Format the message using the parent class format method
        original_message = super().format(record)
        
        # Truncate the message if it exceeds the max_length
        if len(original_message) > self.max_length:
            truncated_message = original_message[:self.max_length] + '...'
            record.message = truncated_message
        else:
            record.message = original_message
        
        return record.message

log_directory = "logs"  # Replace with your actual log directory path

formatter = TruncateFormatter(
    fmt='%(asctime)s - %(levelname)s - %(message)s',
    max_length=400  # Set the maximum length for log messages
)

file_handler = logging.FileHandler(f"{log_directory}/app.log")
file_handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[file_handler]
)

def main(assistant_type):
    logging.info(f"Creating assistant of type: {assistant_type}")
    medical_assistant = create_assistant(assistant_type="medical", model='gpt-3.5-turbo', temperature=1, top_p=1)
    lunch_assistant = create_assistant(assistant_type="lunch", model='gpt-3.5-turbo', temperature=1, top_p=1)
    router = ConversationRouter([medical_assistant, lunch_assistant])

    if hasattr(medical_assistant, 'get_initial_message'):
        initial_message = medical_assistant.get_initial_message()
        print(f"{Fore.LIGHTBLUE_EX}Assistant:{Style.RESET_ALL} {initial_message}")
    else:
        print(f"{Fore.LIGHTBLUE_EX}Assistant:{Style.RESET_ALL} Hello! How can I assist you today? (type 'exit' to end the conversation)")

    while True:
        user_input = input(f"{Fore.LIGHTGREEN_EX}You: {Style.RESET_ALL}")
        if user_input.lower() == 'exit':
            print(f"{Fore.LIGHTBLUE_EX}Assistant:{Style.RESET_ALL} Goodbye!")
            break
        response = router.route(user_input)
        print(f"{Fore.LIGHTBLUE_EX}Assistant:{Style.RESET_ALL} {response}")
        logging.info(f"User input: {user_input}")
        logging.info(f"Assistant response: {response}")

if __name__ == '__main__':
    # Set default assistant type to "medical" if no argument is provided
    assistant_type = "medical" if len(sys.argv) < 2 else sys.argv[1]
    logging.info(f"Running main with assistant_type: {assistant_type}")
    main(assistant_type)

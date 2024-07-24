# ./main.py

import sys
import logging
import os
from colorama import Fore, Style, init
from assistants.assistant_factory import create_assistant
from router.conversation_router import ConversationRouter
from assistants.lunch.lunch_assistant import LunchAssistant  # Corrected import path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'assistants')))

init(autoreset=True)

log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{log_directory}/app.log")
    ]
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

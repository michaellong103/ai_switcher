# ./build_system_message.py
import os
import json
from .compress_json import compress_json  # Import the compress_json function
from .initial_message_creator import create_initial_message  # Import the initial message function

def build_system_message_file():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Compress the original JSON file before building the system message
    json_file_path = os.path.join(current_dir, '..', '..', 'API_response', 'final_question_output.json')
    compressed_json_path = os.path.join(current_dir, 'compressed_final_question_output.json')
    
    compress_json(json_file_path, compressed_json_path)

    # Load the compressed_final_question_output.json file
    try:
        with open(compressed_json_path, 'r') as f:
            question_data = json.load(f)
        print(f'Successfully loaded JSON from {compressed_json_path}')
    except FileNotFoundError:
        print(f'Error: File not found: {compressed_json_path}')
        return
    except json.JSONDecodeError:
        print(f'Error: JSON decoding failed for file: {compressed_json_path}')
        return

    # Construct the system message starting with the JSON data
    system_message_content = (
        f'Data = {json.dumps(question_data, separators=(",", ":"))}\n\n'
        "The data has been provided to you in JSON. Please ask the questions in order.\n"
        "Requirement:\n"
        "(1) Ask one question with possible answers at a time.\n"
        "(2) Number any possible answers to a question rather than using bullet points.\n"
        "(3) Be sure to confirm the answer.\n"
        "(4) After the user (You) answers a question, the next question asked by the assistant should be the confirmation question.\n"
        "(5) The user (You) must first answer the question with a number or integer and then confirm the answer in the next question with a (Y/N).\n"
        "(6) \"Confirmed\" must be included exactly in the response to the Confirm y/n message.\n"
        "(7) Ask one question at a time: Present only one question to the patient along with its possible answers.\n"
        "(8) Number the possible answers: Instead of using bullet points, provide the possible answers as a numbered list (e.g., 1, 2, 3).\n"
        "(9) Sequence of questions: After the patient selects an answer, immediately ask a separate confirmation question based on their selection before moving on to the next main question.\n"
        "(10) The word 'Confirmed' must be included exactly in the response to the 'Confirm (y/n)' message.\n"
        "(11) Confirmation format: The confirmation should be framed as a question, such as: 'You selected [Answer]. Is that correct? (Y/N)'\n"
        "(12) Response requirement: The patient must first respond to the initial question with a number (or integer) corresponding to their choice. Then, they must answer the confirmation question with a simple 'Y' (yes) or 'N' (no).\n"
        "(13) Always keep the options or answers to each question in a logical order. (Phase 1, Phase 2, Phase 3, etc... )\n"
        "(14) Ensure that the logical order is maintained for consistency across all questions.\n\n"
    )

    # Append the content of examples.txt to the system message content
    examples_file_path = os.path.join(current_dir, 'examples.txt')
    try:
        with open(examples_file_path, 'r') as examples_file:
            examples_content = examples_file.read()
            system_message_content += f"{examples_content}\n"
    except FileNotFoundError:
        print(f'Warning: {examples_file_path} not found. Skipping appending examples.')

    # Create the initial message using the imported function
    initial_message = create_initial_message()

    # Define the path to write the system_message.py file
    system_message_file_path = os.path.join(current_dir, 'system_message.py')
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(system_message_file_path), exist_ok=True)

    # Write the content to system_message.py
    with open(system_message_file_path, 'w') as file:
        file.write(f'system_message = {{"role": "system", "content": """{system_message_content}"""}}\n\n')
        file.write(f'initial_message = """{initial_message}"""\n')

    print(f'Configuration file {system_message_file_path} built successfully.')

if __name__ == "__main__":
    build_system_message_file()

# ./assistants/base_assistant.py
import requests
import time
import logging
from colorama import Fore
from config import API_URL, headers

class BaseAssistant:

    def __init__(self, system_message, model, temperature, top_p):
        if not system_message or not isinstance(system_message, dict) or 'role' not in system_message or ('content' not in system_message):
            raise ValueError("System message must be a dict with 'role' and 'content' fields.")
        self.system_message = system_message
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.conversation_history = [self.system_message]
        logging.info(f'Initialized BaseAssistant with system_message: {self.system_message}')

    def get_response(self, user_input):
        self.conversation_history.append({'role': 'user', 'content': user_input})
        logging.info(f'Updated conversation_history: {self.conversation_history}')
        max_retries = 5
        retry_delay = 1
        assistant_message = "I'm sorry, I'm currently experiencing issues. Please try again later."
        for attempt in range(max_retries):
            try:
                payload = {'model': self.model, 'messages': self.conversation_history, 'temperature': self.temperature, 'top_p': self.top_p}
                logging.info(f'Sending request to OpenAI API: {payload}')
                response = requests.post(API_URL, headers=headers, json=payload)
                response.raise_for_status()
                completion = response.json()
                assistant_message = completion['choices'][0]['message']['content']
                logging.info(f'Received response from OpenAI API: {assistant_message}')
                break
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    error_content = response.json()
                    if error_content['error']['code'] == 'insufficient_quota':
                        logging.error(f'Quota exceeded: {error_content['error']['message']}')
                        return assistant_message
                    logging.warning(f'Rate limit exceeded. Retrying in {retry_delay} seconds...')
                    time.sleep(retry_delay)
                    retry_delay *= 2
                elif response.status_code == 404:
                    logging.error(f'404 Not Found: The endpoint does not exist. Please check the API URL.')
                    return assistant_message
                else:
                    logging.error(f'HTTP Error: {e}')
                    logging.error(f'Response content: {response.content}')
                    logging.error(f'Request payload: {payload}')
                    assistant_message = f'An error occurred: {e}'
                    break
            except Exception as e:
                logging.error(f'Exception: {e}')
                assistant_message = f'An error occurred: {e}'
                break
        self.conversation_history.append({'role': 'assistant', 'content': assistant_message})
        return assistant_message

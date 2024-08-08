# ./config.py
import os

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'sk-proj-EtqOVSzBg9hjVpTj6J3hT3BlbkFJGqzDX97GDYm7L5lweRPW')  # Replace with your actual OpenAI API key
API_URL = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

init_variables = {
    "distance": 100,
    "maxTrial": 20,
    "minTrial": 5
}

start_distance = "10 miles"
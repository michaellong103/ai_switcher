# test_display_in_terminal.py

import os
import sys

# Add the parent directory to the Python path to access display_in_terminal and interfaces modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from display_in_terminal.main import main as display_main

# Define the display types and the path to the JSON file
display_types = ["condensed", "detailed", "questions"]
json_path = "./API_response/output_final_big.json"

# Function to test the main function with the given display type
def run_test(display_type, json_path):
    print(f"Testing display type: {display_type}")
    display_main(display_type, json_path)
    print("="*80)

# Run the tests for each display type
for display_type in display_types:
    run_test(display_type, json_path)

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from display_in_terminal.main import main as display_main
display_types = ['condensed', 'detailed', 'questions']
json_path = './API_response/output_final_big.json'

def run_test(display_type, json_path):
    print(f'Testing display type: {display_type}')
    display_main(display_type, json_path)
    print('=' * 80)
for display_type in display_types:
    run_test(display_type, json_path)

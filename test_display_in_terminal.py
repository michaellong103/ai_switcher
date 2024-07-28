# test_display_in_terminal.py

import subprocess

# Define the display types and the path to the JSON file
display_types = ["condensed", "detailed", "questions"]
json_path = "./API_response/output_final_big.json"
main_script_path = "./display_in_terminal/main.py"

# Function to run the main.py script with the given display type
def run_test(display_type, json_path):
    try:
        result = subprocess.run(
            ["python3", main_script_path, display_type, json_path],
            capture_output=True,
            text=True,
            check=True,
            timeout=60  # Add a timeout to prevent indefinite freezing
        )
        print(f"Testing display type: {display_type}")
        print(result.stdout)
        print("="*80)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while testing display type: {display_type}")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.output}")
        print(f"Error: {e.stderr}")
        print("="*80)
    except subprocess.TimeoutExpired:
        print(f"Testing display type: {display_type} timed out.")
        print("="*80)

# Run the tests for each display type
for display_type in display_types:
    run_test(display_type, json_path)

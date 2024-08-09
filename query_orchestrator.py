# ./query_orchestrator.py
import os
import logging
from API_query.clinical_trials_query import main as clinical_trials_query_main



def run_query_and_evaluate(input_file_path, config_file_path, output_file_path_1, output_file_path_2):
    """Runs the clinical trial query and returns the success status."""
    logging.info("Running clinical trials query.")
    success = clinical_trials_query_main(input_file_path, config_file_path, output_file_path_1, output_file_path_2)
    return success

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, 'API_query', 'input.json')
    output_file_path_1 = os.path.join(script_dir, 'API_query', 'output.json')
    output_file_path_2 = os.path.join(script_dir, 'API_response', 'finaloutput.json')
    config_file_path = os.path.join(script_dir, 'config_state.json')

    max_radius = 500
    radius_increment = 50
    current_radius = 10

    # Run initial query and evaluation
    success = run_query_and_evaluate(input_file_path, config_file_path, output_file_path_1, output_file_path_2)

    # Loop until successful query or maximum radius reached
    while not success and current_radius < max_radius:
        current_radius += radius_increment
        logging.info(f"Increasing search radius to {current_radius} km and retrying.")
        
        # Update radius in config
        # Assuming you have logic to update the radius in the config
        # For example, you can write a function to update the input JSON or config state with the new radius

        # Re-run the query and evaluation
        success = run_query_and_evaluate(input_file_path, config_file_path, output_file_path_1, output_file_path_2)

    if not success:
        logging.info("No trials found after maximum radius expansion. Exiting process.")

if __name__ == '__main__':
    main()

# ./sorter_trials_to_ai/sort_data.py

import sys
import os
import logging
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def run_timespan_phase():
    """Phase 1: Run the TimeSpan calculations (dynamic_timespans)."""
    logging.info("Starting Phase 1: Running TimeSpan calculations (dynamic_timespans)")
    
    try:
        logging.debug("Executing dynamic_timespans/main.py script")
        subprocess.run(['python', 'dynamic_timespans/main.py'], check=True)
        logging.info("Completed Phase 1: TimeSpan calculations finished.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to run dynamic_timespans script: {e}")
        raise

def run_phases_phase():
    """Phase 2: Run the Phases calculations (dynamic_phases)."""
    logging.info("Starting Phase 2: Running Phases calculations (dynamic_phases)")
    
    try:
        logging.debug("Executing dynamic_phases/dynamic_phases.py script")
        subprocess.run(['python', 'dynamic_phases/dynamic_phases.py'], check=True)
        logging.info("Completed Phase 2: Phases calculations finished.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to run dynamic_phases script: {e}")
        raise

def calculate_questions_phase():
    """Phase 3: Calculate which questions to run."""
    logging.info("Starting Phase 3: Calculating which questions to run (Placeholder)")
    subprocess.run(['python', 'questions_calculation/main.py'], check=True)
    # Debug placeholder logic for future implementation
    logging.debug("No questions logic implemented yet")
    logging.info("Completed Phase 3: Question calculations finished.")

def create_new_ai_phase():
    """Phase 4: Create new AI from Questions."""
    logging.info("Starting Phase 4: Creating new AI from Questions (Placeholder)")
    # Debug placeholder logic for future implementation
    logging.debug("No AI creation logic implemented yet")
    logging.info("Completed Phase 4: AI creation finished.")

def user_router_phase():
    """Phase 5: User Router to Switch AI."""
    logging.info("Starting Phase 5: User Router to Switch AI (Placeholder)")
    # Debug placeholder logic for future implementation
    logging.debug("No user routing logic implemented yet")
    logging.info("Completed Phase 5: User routing finished.")

def sort_trials_data():
    """Main function to execute all phases in sequence."""
    logging.info("Starting sort_trials_data sequence")

    try:
        logging.debug("Running all phases sequentially")
        run_timespan_phase()
        run_phases_phase()
        calculate_questions_phase()
        create_new_ai_phase()
        user_router_phase()

        logging.info("All phases completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during the execution of sort_trials_data: {e}")
        raise

if __name__ == "__main__":
    # Calling the main function now named sort_trials_data
    sort_trials_data()

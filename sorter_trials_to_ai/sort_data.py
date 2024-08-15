import sys
import os
import logging
import subprocess

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configuring logging for the application
logging.basicConfig(level=logging.INFO)

def run_timespan_phase():
    """Phase 1: Run the TimeSpan calculations (dynamic_timespans)."""
    logging.info("Starting Phase 1: Running TimeSpan calculations (dynamic_timespans)")
    
    # Run the dynamic_timespans script using subprocess
    subprocess.run(['python', 'dynamic_timespans/main.py'], check=True)
    
    logging.info("Completed Phase 1: TimeSpan calculations finished.")

def run_phases_phase():
    """Phase 2: Run the Phases calculations (dynamic_phases)."""
    logging.info("Starting Phase 2: Running Phases calculations (dynamic_phases)")
    
    # Run the dynamic_phases script using subprocess
    subprocess.run(['python', 'dynamic_phases/dynamic_phases.py'], check=True)
    
    logging.info("Completed Phase 2: Phases calculations finished.")

def calculate_questions_phase():
    """Phase 3: Calculate which questions to run."""
    logging.info("Starting Phase 3: Calculating which questions to run (Placeholder)")
    # Placeholder for question calculation logic
    logging.info("Completed Phase 3: Question calculations finished.")

def create_new_ai_phase():
    """Phase 4: Create new AI from Questions."""
    logging.info("Starting Phase 4: Creating new AI from Questions (Placeholder)")
    # Placeholder for AI creation logic
    logging.info("Completed Phase 4: AI creation finished.")

def user_router_phase():
    """Phase 5: User Router to Switch AI."""
    logging.info("Starting Phase 5: User Router to Switch AI (Placeholder)")
    # Placeholder for user routing logic
    logging.info("Completed Phase 5: User routing finished.")

def main():
    """Main function to execute all phases in sequence."""
    logging.info("Starting the application")

    try:
        run_timespan_phase()
        run_phases_phase()
        calculate_questions_phase()
        create_new_ai_phase()
        user_router_phase()

        logging.info("All phases completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

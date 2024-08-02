# ./API_actions/async_caller_program.py

import json
import logging

def process_async_caller(input_file, output_file):
    """
    Processes the input file and writes the results to the output file.
    """
    try:
        # Load the input data
        with open(input_file, 'r') as infile:
            data = json.load(infile)

        # Perform some processing (replace this with actual processing logic)
        processed_data = perform_complex_logic(data)

        # Write the processed data to the output file
        with open(output_file, 'w') as outfile:
            json.dump(processed_data, outfile, indent=4)

        logging.info("async_caller_program.py: Data processed successfully.")
        return 0, "Processing complete"

    except Exception as e:
        logging.error(f"async_caller_program.py: Error processing data: {e}", exc_info=True)
        return 1, str(e)

def perform_complex_logic(data):
    """
    Example logic to process the data.
    This should be replaced with the actual processing logic required.
    """
    # Example processing: Add a new key to the dictionary
    data['processed'] = True
    return data

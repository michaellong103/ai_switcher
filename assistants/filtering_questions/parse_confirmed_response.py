# ./parse_confirmed_response.py
import logging
import traceback

class ConfirmedResponseParser:
    def __init__(self, output_file='confirmed_responses.txt'):
        self.output_file = output_file
        logging.info(f"Initialized ConfirmedResponseParser with output file: {self.output_file}")
        print(f"\033[96m[DEBUG]\033[0m Initialized ConfirmedResponseParser with output file: {self.output_file}")

    def store_response(self, response):
        """
        Stores the confirmed response to a file.
        """
        try:
            # Attempt to open the file and write the response
            with open(self.output_file, 'a') as file:
                file.write(response + '\n')
            
            # Log and print detailed success information
            logging.info(f"Successfully stored response to {self.output_file}")
            print(f"\033[92m[INFO]\033[0m Successfully stored response to {self.output_file}: {response}")

        except Exception as e:
            # Log the error with traceback and print detailed error information
            logging.error(f"Failed to store response to {self.output_file}. Error: {e}")
            logging.error(traceback.format_exc())
            print(f"\033[91m[ERROR]\033[0m Failed to store response to {self.output_file}")
            print(f"\033[91m[ERROR]\033[0m Exception details: {e}")
            print(f"\033[91m[ERROR]\033[0m Stack trace:\n{traceback.format_exc()}")

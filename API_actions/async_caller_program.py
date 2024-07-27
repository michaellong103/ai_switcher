# ./API_actions/async_caller_program.py
import asyncio
import subprocess
import json
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def call_api_query(input_file, output_file):
    if not os.path.exists(input_file):
        logging.error(f"Error: The input file '{input_file}' does not exist.")
        return 1, None

    process = await asyncio.create_subprocess_exec(
        'python', 'api_query.py', input_file, output_file,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Wait for the process to complete and capture output
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        logging.info("api_query.py completed successfully.")
    else:
        logging.error(f"api_query.py failed with return code {process.returncode}.")

    # Output the captured stderr (if any)
    if stderr:
        logging.error(f"Script Errors:\n {stderr.decode()}")

    # Try to parse the API response from the stdout
    try:
        api_response = json.loads(stdout.decode())
    except json.JSONDecodeError:
        api_response = None

    return process.returncode, api_response

async def main(input_file, output_file):
    return_code, api_response = await call_api_query(input_file, output_file)
    
    if return_code == 0:
        logging.info("The API call is complete, and the files have been written successfully.")
        response_message = "Loading new data completed successfully."
    else:
        logging.error("There was an issue with the API call.")
        if api_response is None:
            logging.error("Failed to decode the API response as JSON.")
        response_message = "Loading new data failed."

    return response_message

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python async_caller_program.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    response_message = asyncio.run(main(input_file, output_file))
    print(response_message)

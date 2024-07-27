import os
import asyncio
import logging

async def call_async_caller(input_file, output_file):
    # Resolve the path to async_caller_program.py
    async_caller_script = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'API_action', 'async_caller_program.py'))

    process = await asyncio.create_subprocess_exec(
        'python', async_caller_script, input_file, output_file,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # Wait for the process to complete and capture output
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        logging.info("async_caller_program.py completed successfully.")
    else:
        logging.error(f"async_caller_program.py failed with return code {process.returncode}.")

    if stderr:
        logging.error(f"Script Errors:\n {stderr.decode()}")

    return process.returncode, stdout.decode()

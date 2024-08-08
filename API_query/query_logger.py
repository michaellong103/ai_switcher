# ./API_query/query_logger.py

import logging
import os

LOG_FILE_PATH = "query_log.txt"
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_query(query_url, input_data):
    """
    Log the query details to the query log file.

    :param query_url: The constructed query URL
    :param input_data: The input data used for constructing the query
    """
    # Create log message
    log_message = (
        f"Query URL: {query_url}\n"
        f"Input Data: {input_data}\n"
        f"{'-'*80}"
    )

    # Log the message
    logging.info(log_message)

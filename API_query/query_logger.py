# ./API_query/query_logger.py
import logging
import os
LOG_FILE_PATH = 'query_log.txt'
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_query(query_url, input_data):
    log_message = f'Query URL: {query_url}\nInput Data: {input_data}\n{'-' * 80}'
    logging.info(log_message)

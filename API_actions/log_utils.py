# ./API_actions/log_utils.py
import logging
import json

def log_query_details(query_details, stats, log_file='query_log.json'):
    logging.debug(f"Logging query details to {log_file}")
    try:
        log_data = {
            "query_details": query_details,
            "stats": stats
        }
        with open(log_file, 'a') as file:
            json.dump(log_data, file, indent=4)
            file.write("\n")
    except Exception as e:
        logging.error(f"Error logging query details: {e}", exc_info=True)


def clear_log_file(log_file='query_log.json'):
    logging.debug(f"Clearing log file: {log_file}")
    try:
        open(log_file, 'w').close()
    except Exception as e:
        logging.error(f"Error clearing log file: {e}", exc_info=True)

# ./logging_config.py
import logging
import os
import json

class TruncateFormatter(logging.Formatter):

    def __init__(self, fmt=None, datefmt=None, style='%', max_length=100):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.max_length = max_length
        self.color_map = {}
        self.color_palette = ['#FF5733', '#33FF57', '#3357FF', '#FF33A6', '#FFC733', '#33FFF2', '#8D33FF', '#FF8233', '#FFB533', '#33FF99', '#3399FF', '#FF3399', '#FFD433', '#33FFD1', '#A833FF', '#FF5733', '#FFBD33', '#33FF66', '#33CCFF', '#FF3366', '#FFDD33', '#33FFE5', '#C733FF', '#FF6F33', '#FFA833', '#33FF44', '#3385FF', '#FF3385', '#FFF233', '#33FFFA', '#B833FF', '#FF7733', '#FF9433', '#33FFB5', '#337AFF', '#FF337A', '#FFEA33', '#33FFEB', '#9A33FF']

    def get_color_for_folder(self, folder_name):
        if folder_name not in self.color_map:
            color_index = len(self.color_map) % len(self.color_palette)
            self.color_map[folder_name] = self.color_palette[color_index]
        return self.color_map[folder_name]

    def format(self, record):
        path_parts = os.path.normpath(record.pathname).split(os.sep)
        if len(path_parts) > 1:
            parent_folder = path_parts[-2]
        else:
            parent_folder = 'root'
        filename = os.path.basename(record.pathname)
        record.parent_and_file = f'{parent_folder}/{filename}'
        color = self.get_color_for_folder(parent_folder)
        original_message = super().format(record)
        colored_message = f"<span style='color:{color}'>[{parent_folder}]</span> {original_message}"
        if len(colored_message) > self.max_length:
            truncated_message = colored_message[:self.max_length] + '...'
            record.message = truncated_message
        else:
            record.message = colored_message
        return record.message

def delete_logs(log_directory='logs'):
    if os.path.exists(log_directory):
        for log_file in os.listdir(log_directory):
            file_path = os.path.join(log_directory, log_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f'Deleted log file: {file_path}')
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')

def delete_items(target_directory='API_response', delete_dirs=False):
    logging.info(f'Cleaning up items in directory: {target_directory}')
    if os.path.exists(target_directory):
        for item_name in os.listdir(target_directory):
            item_path = os.path.join(target_directory, item_name)
            try:
                if os.path.isfile(item_path):
                    os.unlink(item_path)
                    logging.info(f'Deleted file: {item_path}')
                elif os.path.isdir(item_path) and delete_dirs:
                    os.rmdir(item_path)
                    logging.info(f'Deleted directory: {item_path}')
            except Exception as e:
                logging.error(f'Failed to delete {item_path}. Reason: {e}')
    else:
        logging.warning(f'Directory does not exist: {target_directory}')

def reset_config_state(config_file_path='config_state.json'):
    empty_state = {'current_api_params': {}, 'last_clinical_trials_api_url': '', 'stats': {}}
    try:
        with open(config_file_path, 'w') as config_file:
            json.dump(empty_state, config_file, indent=4)
        logging.info(f'Config state reset successfully: {config_file_path}')
    except Exception as e:
        logging.error(f'Failed to reset config state: {e}')

def configure_logging():
    log_directory = 'logs'
    os.makedirs(log_directory, exist_ok=True)
    log_format = '%(asctime)s - %(levelname)s - %(parent_and_file)s - %(message)s'
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    if logger.hasHandlers():
        logger.handlers.clear()
    file_handler = logging.FileHandler(os.path.join(log_directory, 'app.log'))
    file_handler.setFormatter(TruncateFormatter(fmt=log_format, max_length=400))
    logger.addHandler(file_handler)

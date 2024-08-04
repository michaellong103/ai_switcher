# ./logging_config.py

import logging
import os

class TruncateFormatter(logging.Formatter):
    """
    Custom formatter that includes the parent directory and file name in log messages
    and truncates messages if they exceed a specified maximum length.
    """
    def __init__(self, fmt=None, datefmt=None, style='%', max_length=100):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.max_length = max_length
        self.color_map = {}
        self.color_palette = [
            "#FF5733",  # Red
            "#33FF57",  # Green
            "#3357FF",  # Blue
            "#FF33A6",  # Pink
            "#FFC733",  # Yellow
            "#33FFF2",  # Cyan
            "#8D33FF",  # Purple
            "#FF8233"   # Orange
        ]

    def get_color_for_folder(self, folder_name):
        """
        Assigns a color to a folder name using a color palette.
        Ensures consistent color usage for each folder.
        """
        if folder_name not in self.color_map:
            # Assign a new color from the palette, cycling if necessary
            color_index = len(self.color_map) % len(self.color_palette)
            self.color_map[folder_name] = self.color_palette[color_index]
        
        return self.color_map[folder_name]

    def format(self, record):
        # Extract the parent directory and filename
        path_parts = os.path.normpath(record.pathname).split(os.sep)
        if len(path_parts) > 1:
            parent_folder = path_parts[-2]  # Get the parent folder name
        else:
            parent_folder = 'root'
        filename = os.path.basename(record.pathname)

        # Create a new attribute to include in the log format
        record.parent_and_file = f"{parent_folder}/{filename}"

        # Get the color based on the parent directory
        color = self.get_color_for_folder(parent_folder)

        # Format the message using the parent class format method
        original_message = super().format(record)

        # Apply color to the formatted message
        colored_message = f"<span style='color:{color}'>[{parent_folder}]</span> {original_message}"

        # Truncate the message if it exceeds the max_length
        if len(colored_message) > self.max_length:
            truncated_message = colored_message[:self.max_length] + '...'
            record.message = truncated_message
        else:
            record.message = colored_message

        return record.message

def delete_logs(log_directory="logs"):
    """
    Deletes all log files in the log directory to ensure clean logs for each run.
    """
    if os.path.exists(log_directory):
        for log_file in os.listdir(log_directory):
            file_path = os.path.join(log_directory, log_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"Deleted log file: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
                
def delete_items(target_directory="API_response", delete_dirs=False):
    """
    Deletes all files (and optionally directories) in the specified target directory.
    
    :param target_directory: Path to the directory where items should be deleted.
    :param delete_dirs: Boolean flag indicating whether to delete directories as well.
    """
    logging.info(f"Cleaning up items in directory: {target_directory}")

    # Check if the target directory exists
    if os.path.exists(target_directory):
        for item_name in os.listdir(target_directory):
            item_path = os.path.join(target_directory, item_name)
            
            try:
                # Delete files
                if os.path.isfile(item_path):
                    os.unlink(item_path)
                    logging.info(f"Deleted file: {item_path}")
                # Optionally delete directories
                elif os.path.isdir(item_path) and delete_dirs:
                    os.rmdir(item_path)
                    logging.info(f"Deleted directory: {item_path}")
            except Exception as e:
                logging.error(f"Failed to delete {item_path}. Reason: {e}")
    else:
        logging.warning(f"Directory does not exist: {target_directory}")

def configure_logging():
    """
    Configures the logging system to output to a file with a custom format that includes
    parent directory and filename, and truncates messages if necessary.
    """
    # Define the log directory and create it if it doesn't exist
    log_directory = "logs"
    os.makedirs(log_directory, exist_ok=True)

    # Define the log format including parent folder and filename
    log_format = '%(asctime)s - %(levelname)s - %(parent_and_file)s - %(message)s'

    # Create a logger
    logger = logging.getLogger()  # Get the root logger

    # Set the logging level
    logger.setLevel(logging.DEBUG)

    # Remove any existing handlers (e.g., default console handler)
    if logger.hasHandlers():
        logger.handlers.clear()

    # Configure the file handler
    file_handler = logging.FileHandler(os.path.join(log_directory, "app.log"))
    file_handler.setFormatter(TruncateFormatter(fmt=log_format, max_length=400))

    # Add the file handler to the logger
    logger.addHandler(file_handler)

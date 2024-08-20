# ./AI_launcher/dynamic_ai_launcher.py

from .json_loader import JSONLoader
import logging

class DynamicAILauncher:
    def __init__(self, config_path):
        """
        Initialize the DynamicAILauncher with the provided configuration path.
        
        :param config_path: Path to the JSON configuration file.
        """
        # Load configuration from the provided JSON file
        config = JSONLoader.load_json(config_path)
        if config:
            # Set up the AI launcher parameters from the config
            self.system_message = config.get("system_message", {})
            self.model = config.get("model", "gpt-3.5-turbo")
            self.temperature = config.get("temperature", 0.7)
            self.top_p = config.get("top_p", 0.9)
        else:
            # Log an error and raise an exception if the config is invalid
            logging.error(f"Failed to load configuration from {config_path}")
            raise ValueError("Invalid configuration")

    def launch(self):
        """
        Launch the AI instance based on the loaded configuration.
        
        :return: Dictionary with the AI instance configuration details.
        """
        # Log the launch details
        logging.info(f"Launching AI with model: {self.model}")
        
        # Return the configuration details as a dictionary
        return {
            "system_message": self.system_message,
            "model": self.model,
            "temperature": self.temperature,
            "top_p": self.top_p
        }

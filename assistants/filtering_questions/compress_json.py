# ./compress_json.py
import json
from .sort_opts_by_phase import sort_opts_by_phase  # Import the sorting function

def compress_json(input_file, output_file):
    """
    Compresses the JSON content by sorting the 'opts' key by phase and removing spaces and line breaks.
    Saves the compressed content to the output file.
    """
    try:
        # Read the JSON content from the input file
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        # Sort the 'opts' key by phase
        data = sort_opts_by_phase(data)
        
        # Compress the JSON content (remove all spaces and line breaks)
        compressed_data = json.dumps(data, separators=(',', ':'))
        
        # Save the compressed JSON content to the output file
        with open(output_file, 'w') as f:
            f.write(compressed_data)
        
        print(f"Compressed JSON has been saved to {output_file}")
    
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {input_file} does not contain valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

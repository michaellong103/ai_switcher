import json
import os

def select_specific_question(input_file, output_file):
    """
    Compresses the JSON content by keeping only the question matching 
    "How long are you willing to commit to a clinical trial" and removing 
    all unnecessary whitespace and line breaks.

    Saves the filtered content to the output file.
    
    Args:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to the output JSON file where the filtered content will be saved.
    """
    try:
        # Read the JSON content from the input file
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        # Filter out the question matching the specified string
        filtered_data = {
            "qs": [
                q for q in data.get("qs", [])
                if "How long are you willing to commit to a clinical trial" in q.get("q", "")
            ]
        }

        # Ensure we found the question
        if not filtered_data["qs"]:
            print("Error: The specified question was not found in the input file.")
            return

        # Compress the filtered JSON content (remove all unnecessary whitespace and line breaks)
        compressed_data = json.dumps(filtered_data, separators=(',', ':'))

        # Save the compressed JSON content to the output file
        with open(output_file, 'w') as f:
            f.write(compressed_data)
        
        print(f"Filtered and compressed JSON has been saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {input_file} does not contain valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Define paths to the input and output files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_json_path = os.path.join(current_dir, 'compressed_final_question_output.json')
    output_json_path = os.path.join(current_dir, 'target_final_question_output.json')

    # Run the function to filter and save the specific question
    select_specific_question(input_json_path, output_json_path)

# ./increase_radius_query/write_input_json.py
import os
import json
import logging


def write_to_input_json(age, gender, medical_condition, location, latitude, longitude, distance):
    logging.info("Starting to write to input.json")
    
    # Directory and file path for the input.json in API_query
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.abspath(os.path.join(script_dir, '..', 'API_query'))
    file_path = os.path.join(target_dir, 'input.json')
    
    logging.debug(f"Target directory: {target_dir}")
    logging.debug(f"File path: {file_path}")

    # Data to be written
    data = {
        "Age": age,
        "Gender": gender,
        "Medical Condition": medical_condition,
        "Location": location,
        "Latitude": latitude,
        "Longitude": longitude,
        "Distance": distance
    }
    
    logging.info(f"Data to be written: {data}")

    try:
        # Ensure directory exists and write to the file
        os.makedirs(target_dir, exist_ok=True)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        logging.info(f"Data successfully written to {file_path}")
    except Exception as e:
        logging.error(f"Failed to write data to {file_path}: {e}")

if __name__ == "__main__":
    # Example data
    write_to_input_json(
        age="50",
        gender="Female",
        medical_condition="Gaucher Disease 333",
        location="Los Angeles, CA",
        latitude="34.0522",
        longitude="-118.2437",
        distance=103
    )

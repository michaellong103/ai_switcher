# utils/json_handler.py

def read_and_format_json(json_input):
    formatted_data = {
        "age": json_input["Age"],
        "gender": json_input["Gender"],
        "condition": json_input["Medical Condition"],
        "location": json_input["Location"],
        "lat": json_input["Latitude"],
        "lon": json_input["Longitude"]
    }
    return formatted_data

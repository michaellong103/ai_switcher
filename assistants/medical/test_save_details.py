# ./assistants/medical/test_save_details.py
import json
import os

details = {
    "Age": "45",
    "Gender": "Female",
    "Medical Condition": "Non-Small Cell Lung Cancer",
    "Location": "Seattle, WA",
    "Latitude": "47.6062",
    "Longitude": "-122.3321"
}

try:
    os.makedirs('assistants/medical', exist_ok=True)
    with open('details.json', 'w') as json_file:
        json.dump(details, json_file, indent=4)
    print("Details saved to details.json")
except Exception as e:
    print(f"Failed to save details to JSON: {e}")

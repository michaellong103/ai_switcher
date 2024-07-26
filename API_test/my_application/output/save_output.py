# output/save_output.py
import os
import json
import csv

def save_output(data, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save as JSON
    json_path = os.path.join(output_dir, "output.json")
    with open(json_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    
    # Save as CSV
    csv_path = os.path.join(output_dir, "output.csv")
    with open(csv_path, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        if isinstance(data, dict):
            # Flatten the dictionary for CSV
            def flatten_dict(d, parent_key="", sep="_"):
                items = []
                for k, v in d.items():
                    new_key = f"{parent_key}{sep}{k}" if parent_key else k
                    if isinstance(v, dict):
                        items.extend(flatten_dict(v, new_key, sep=sep).items())
                    else:
                        items.append((new_key, v))
                return dict(items)
            
            flat_data = flatten_dict(data)
            csv_writer.writerow(flat_data.keys())
            csv_writer.writerow(flat_data.values())
        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            csv_writer.writerow(data[0].keys())
            for item in data:
                csv_writer.writerow(item.values())

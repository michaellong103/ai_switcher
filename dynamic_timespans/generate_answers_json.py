# ./generate_answers_json.py

import json

def read_output_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def generate_options(data):
    total_trials = sum(group["total"] for group in data)
    options = []

    for group in data:
        # Calculate earliest and latest date strings
        earliest_date = parse_date(group["earliestDate"])
        latest_date = parse_date(group["latestDate"])

        earliest_years = (earliest_date - CURRENT_DATE).days // 365
        latest_years = (latest_date - CURRENT_DATE).days // 365

        earliest_months = ((earliest_date - CURRENT_DATE).days % 365) // 30
        latest_months = ((latest_date - CURRENT_DATE).days % 365) // 30

        if earliest_years == latest_years and earliest_months < 6 and latest_months < 6:
            # Both dates within the same year and under 6 months
            earliest_str = f"{earliest_years} year {earliest_months} month{'s' if earliest_months != 1 else ''}"
            latest_str = f"{latest_years} year {latest_months} month{'s' if latest_months != 1 else ''}"
        else:
            # Round to the nearest year
            if earliest_months >= 6:
                earliest_years += 1
            if latest_months >= 6:
                latest_years += 1

            earliest_str = f"{earliest_years} year{'s' if earliest_years != 1 else ''}"
            latest_str = f"{latest_years} year{'s' if latest_years != 1 else ''}"

        option_text = f"{earliest_str} to {latest_str} timespan"

        nct_numbers = [list(trial.keys())[0] for trial in group["nctNumbers"]]
        option = {
            "code": group["trialGroup"].replace(" ", ""),
            "optionText": option_text,
            "count": len(nct_numbers),
            "percentage": round((len(nct_numbers) / total_trials) * 100, 2),
            "NCTNumbers": nct_numbers
        }
        options.append(option)

    return options

def generate_answers_json(data):
    return {
        "category": "dynamic_timespans",
        "question": "Could you select a timeframe for the studies?",
        "options": generate_options(data)
    }

def write_answers_to_file(answers, filename):
    with open(filename, 'w') as file:
        json.dump(answers, file, indent=2)

def main():
    output_data = read_output_data("output_data.json")
    answers_json = generate_answers_json(output_data)
    write_answers_to_file(answers_json, "dynamic_timespans.json")
    print("Output written to dynamic_timespans.json")

if __name__ == "__main__":
    main()

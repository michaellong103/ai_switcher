# ./generate_answers.py
import json

def read_output_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def generate_answers(data):
    answers = []
    for group in data:
        earliest_date_from_today = group["earliestDateFromToday"]
        latest_date_from_today = group["latestDateFromToday"]
        answer = (
            f" "
            f"{earliest_date_from_today} and {latest_date_from_today}"
        )
        answers.append(answer)
    return answers

def write_answers_to_file(answers, filename):
    with open(filename, 'w') as file:
        for answer in answers:
            file.write(answer + '\n')

def main():
    output_data = read_output_data("output_data.json")
    answers = generate_answers(output_data)
    write_answers_to_file(answers, "answers.txt")
    for answer in answers:
        print(answer)

if __name__ == "__main__":
    main()

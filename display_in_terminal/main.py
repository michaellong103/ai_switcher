# main.py

from interfaces.interface_generator import generate_interfaces

# Load JSON data from a file
with open('output_final_big.json', 'r') as file:
    trials_json = file.read()

condensed, detailed, questions = generate_interfaces(trials_json)

print(condensed)
print(detailed)
print(questions)

import os
import re

def remove_docstrings_from_file(file_path):

    with open(file_path, 'r') as file:
        content = file.read()

    # Regex pattern to match triple-quoted docstrings (both """ and ''')
    docstring_pattern = re.compile(r'^\s*(?:(?:\'\'\'|""").*?(?:\'\'\'|"""))', re.DOTALL | re.MULTILINE)

    # Remove docstrings
    new_content = docstring_pattern.sub('', content)

    with open(file_path, 'w') as file:
        file.write(new_content)

def process_directory(directory):

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}")
                remove_docstrings_from_file(file_path)

if __name__ == '__main__':
    directory_to_process = '.'  # Current directory
    process_directory(directory_to_process)

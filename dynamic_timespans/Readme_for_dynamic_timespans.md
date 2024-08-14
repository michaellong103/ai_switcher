# Trial Data Processing Application

This application processes clinical trial data, sorts the trials, groups them, calculates additional data, and generates various output formats.

## Table of Contents

- [Overview](#overview)
- [Directory Structure](#directory-structure)
- [Setup](#setup)
- [Usage](#usage)
- [Application Flow](#application-flow)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Overview

The application processes clinical trial data from JSON files, sorts and groups the trials, calculates additional data such as date spans and days until completion, and generates outputs in both text and JSON formats.

## Directory Structure

.
├── answers.json
├── answers.txt
├── calculate_data.py
├── compare_data.py
├── data_processing.py
├── date_utils.py
├── divide_groups.py
├── dynamic_timespans.json
├── generate_answers.py
├── generate_answers_json.py
├── json_utils.py
├── load_data.py
├── main.py
├── original_data.json
├── output_data.json
├── run_main.py
├── sort_data.py
├── testing
│ ├── test_days_until_end.py
│ ├── test_group_sequential_dates.py
│ ├── test_output.py
└── trial_utils.py

markdown
Copy code

## Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. **Install required packages**:
    Ensure you have Python 3.8+ installed. Install any required packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

3. **Ensure data files are in place**:
    - `original_data.json`: Source data for the application.
    - Ensure other data files are placed in the root directory as needed.

## Usage

To start the application, run:

```bash
python run_main.py
This command will load the data, process it, and generate the output files (output_data.json, answers.txt, dynamic_timespans.json).

Application Flow
run_main.py:

Entry point of the application.
Calls the main() function from main.py.
main.py:

Orchestrates the data processing workflow.
Loads data using load_data.py.
Sorts trials using sort_data.py.
Divides trials into groups using divide_groups.py.
Calculates additional data using calculate_data.py.
Writes the processed data to output_data.json.
Data Loading:

load_data.py: Reads data from original_data.json.
Data Processing:

sort_data.py: Sorts trials by daysUntilEnd.
divide_groups.py: Divides trials into groups based on their count.
calculate_data.py: Calculates statistics, formats dates, and computes date spans for each group.
Output Generation:

generate_answers.py: Generates answers from processed data and writes to answers.txt.
generate_answers_json.py: Generates JSON-formatted answers and writes to dynamic_timespans.json.
Testing
Tests are located in the testing directory. To run the tests:

bash
Copy code
python testing/test_days_until_end.py
python testing/test_group_sequential_dates.py
python testing/test_output.py
These tests validate various aspects of the data processing pipeline, including the calculation of daysUntilEnd, sequential group dates, and overall output validation.

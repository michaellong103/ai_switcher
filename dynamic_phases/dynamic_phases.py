# ./testing/test_nct_comparison.py

import os
import argparse
from collections import defaultdict
from json_utils import load_json_data, save_json_data  # Import from the same directory

def categorize_phases(data):
    """Categorizes and counts study phases from the input data, including NCT numbers."""
    phase_counts = defaultdict(lambda: {'count': 0, 'nct_numbers': set()})
    no_phase_entries = []

    for entry in data:
        study_phases = entry.get('studyPhases', [])
        nct_number = entry.get('nctNumber', 'Unknown')
        
        if study_phases:
            for phase in study_phases:
                phase_counts[phase]['count'] += 1
                phase_counts[phase]['nct_numbers'].add(nct_number)
        else:
            no_phase_entries.append(nct_number)
    
    return phase_counts, no_phase_entries

def integrate_questions(category_percentages, template_data):
    """Integrates question categories from the template into the generated output."""
    for field, values in category_percentages.items():
        for question_category in template_data.get('question_categories', []):
            if field == question_category.get('category'):
                for option in question_category.get('options', []):
                    code = option.get('code')
                    if code in values:
                        values[code].update({
                            "optionText": option.get("optionText", ""),
                            "total_after_elimination": option.get("total_after_elimination", None)
                        })

def generate_phase_output(input_path, output_path, template_path):
    """Processes the input data and generates the phase question output."""
    data = load_json_data(input_path)
    template_data = load_json_data(template_path)
    
    if not data:
        print(f"Error: No data found in {input_path}")
        return
    if not template_data:
        print(f"Error: No template data found in {template_path}")
        return

    phase_counts, no_phase_entries = categorize_phases(data)
    total_studies = len(data)
    
    phase_percentages = {
        phase: {
            "percentage": (info['count'] / total_studies) * 100,
            "NCTNumbers": list(info['nct_numbers']),
            "NCTCount": info['count']
        }
        for phase, info in phase_counts.items()
    }

    # Prepare output format similar to SearchCrit.json format
    category_percentages = {
        "studyPhases": phase_percentages
    }

    # Integrate questions from the template
    integrate_questions(category_percentages, template_data)

    output_data = {
        "question": "Which phase are you interested in?",
        "options": list(category_percentages['studyPhases'].values())
    }

    if no_phase_entries:
        output_data["no_phase_entries"] = {
            "count": len(no_phase_entries),
            "NCTNumbers": no_phase_entries,
            "description": "These studies do not have a phase listed."
        }

    save_json_data(output_path, output_data)
    print(f"Phase question output saved to {output_path}")

# Main block for script execution
if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate phase question output from input data.")
    
    # Add arguments for paths
    parser.add_argument('--input', default='/Users/jtc/Documents/o-jobs/GPTs/clinical-trials-GPT/ai_switcher/API_response/dynamic_questions_input.json', help="Path to the input JSON file")
    parser.add_argument('--output', default='/Users/jtc/Documents/o-jobs/GPTs/clinical-trials-GPT/ai_switcher/API_response/phase_question_output.json', help="Path to the output JSON file")
    parser.add_argument('--template', default='/Users/jtc/Documents/o-jobs/GPTs/clinical-trials-GPT/ai_switcher/dynamic_phases/questions_template.json', help="Path to the template JSON file")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute the main function with the provided or default paths
    generate_phase_output(args.input, args.output, args.template)

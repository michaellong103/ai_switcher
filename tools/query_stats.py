# ./tools/query_stats.py
import json
import logging
import os

def extract_trial_info(node):
    nct_ids = []
    brief_titles = []
    if isinstance(node, dict):
        if 'nctId' in node:
            nct_ids.append(node['nctId'])
        if 'briefTitle' in node:
            brief_titles.append(node['briefTitle'])
        for key, value in node.items():
            child_nct_ids, child_brief_titles = extract_trial_info(value)
            nct_ids.extend(child_nct_ids)
            brief_titles.extend(child_brief_titles)
    elif isinstance(node, list):
        for item in node:
            child_nct_ids, child_brief_titles = extract_trial_info(item)
            nct_ids.extend(child_nct_ids)
            brief_titles.extend(child_brief_titles)
    return (nct_ids, brief_titles)

def count_trials(input_file='API_response/output_final_big.json', output_file='API_response/trials_summary.json'):
    try:
        with open(input_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        logging.error(f'File {input_file} not found.')
        return
    except json.JSONDecodeError:
        logging.error(f'Error decoding JSON from file {input_file}.')
        return
    nct_ids, brief_titles = extract_trial_info(data)
    num_trials = len(nct_ids)
    logging.info(f'Number of trials found: {num_trials}')
    logging.info(f'NCT IDs: {nct_ids}')
    logging.info(f'Brief Titles: {brief_titles}')
    summary = {'num_trials': num_trials, 'nct_ids': nct_ids, 'brief_titles': brief_titles}
    try:
        with open(output_file, 'w') as file:
            json.dump(summary, file, indent=4)
    except Exception as e:
        logging.error(f'Error writing to file {output_file}: {e}')
    return summary
if __name__ == '__main__':
    log_directory = os.path.join(os.path.dirname(__file__), '..', 'logs')
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    count_trials()

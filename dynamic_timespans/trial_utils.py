# ./trial_utils.py
def get_all_nct_numbers(trials):
    nct_numbers = set()
    for trial in trials:
        if isinstance(trial, dict):
            for key in trial:
                if isinstance(trial[key], dict) and 'nctNumber' in trial[key]:
                    nct_numbers.add(trial[key]['nctNumber'])
                elif 'NCT' in key:  # Assuming NCT number could be in the key
                    nct_numbers.add(key)
    return nct_numbers
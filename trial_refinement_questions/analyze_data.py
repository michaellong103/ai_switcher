# ./trial_refinement_questions/analyze_data.py

def analyze_data(trials_data):
    # Count distinct dates, only if the 'date' key exists in the trial
    date_filter_count = len(set(trial['date'] for trial in trials_data if 'date' in trial))

    # Count distinct phases, only if the 'phase' key exists in the trial
    phase_filter_count = len(set(trial['phase'] for trial in trials_data if 'phase' in trial))
    
    if date_filter_count < phase_filter_count:
        return 'date'
    else:
        return 'phase'

def ask_user_for_filtering_option(best_option):
    print(f"Based on the analysis, filtering by '{best_option}' might be more effective.")
    choice = input(f"Do you want to filter by '{best_option}' or the other option? (type 'date' or 'phase'): ")
    return choice.strip().lower()

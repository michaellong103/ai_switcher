# ./display_in_terminal/interfaces/interface_generator.py

import json
import logging
from .palette import CYAN, YELLOW, RESET_COLOR

def banner(text):
    return f"{CYAN}{'=' * 40}\n{text}\n{'=' * 40}{RESET_COLOR}"

def condensed_trials(trials):
    output = f"{banner(f'Condensed Trials: ({len(trials)} trials)')}\n\n"
    for i, trial in enumerate(trials, 1):
        title = trial['briefTitle']
        nct_id = trial['nctNumber']
        output += f"{i}. {CYAN}{title}{RESET_COLOR}\n   {YELLOW}{nct_id}{RESET_COLOR}\n\n"
    return output

def detailed_trials(trials):
    output = f"{banner(f'Detailed Trials: ({len(trials)} trials)')}\n\n"
    for i, trial in enumerate(trials, 1):
        title = trial['briefTitle']
        description = trial['briefSummary']
        nct_id = trial['nctNumber']
        output += f"{i}. {CYAN}{title}{RESET_COLOR}\n   {description}\n   {YELLOW}{nct_id}{RESET_COLOR}\n\n"
    return output

def question_format(trials):
    output = f"{banner(f'Question Format: ({len(trials)} trials)')}\n\n"
    output += f"""
{CYAN}Would you like to explore early-stage trials focused on safety, or later-stage trials that look at how well a treatment works?{RESET_COLOR}
1. {CYAN}Phase 1 (highest risk):{RESET_COLOR} These trials focus on assessing the safety of a new treatment, determining appropriate dosage, and identifying potential side effects with a small group of participants.
2. {CYAN}Phase 2 (moderate risk):{RESET_COLOR} These trials evaluate the effectiveness of the treatment and further assess its safety, involving a larger group of participants and providing preliminary data on how well the treatment works.
3. {CYAN}Phase 3 (lower risk):{RESET_COLOR} These trials compare the new treatment to the current standard treatment, involving a large number of participants and providing comprehensive data on effectiveness while monitoring side effects on a larger scale.
4. {CYAN}Phase 4 (lowest risk):{RESET_COLOR} These trials occur after the treatment has been approved for general use and aim to gather additional information on the treatment's long-term effectiveness and safety.
"""  # Properly close the triple-quoted string here
    return output
# ./API_actions/process_api_response.py
import logging

def process_api_response(api_response):
    logging.debug("Processing API response")
    try:
        studies = []
        if isinstance(api_response, dict) and 'studies' in api_response:
            studies = api_response['studies']
        elif isinstance(api_response, list):
            studies = api_response

        num_trials = len(studies)
        trial_names = []
        nct_numbers = []

        for study in studies:
            protocol_section = study.get('protocolSection', {})
            identification_module = protocol_section.get('identificationModule', {})
            
            brief_title = identification_module.get('briefTitle', 'N/A')
            nct_id = identification_module.get('nctId', 'N/A')
            
            trial_names.append(brief_title)
            nct_numbers.append(nct_id)

        stats = {
            "number_of_trials": num_trials,
            "trial_names": trial_names,
            "nct_numbers": ",".join(nct_numbers)
        }

        # Log the details
        logging.info(f"Number of trials: {num_trials}")
        logging.info(f"Trial names: {trial_names}")
        logging.info(f"NCT numbers: {nct_numbers}")

        return stats

    except Exception as e:
        logging.error(f"Error processing API response: {e}", exc_info=True)
        return {}

# ./API_actions/response_processor.py
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
        missing_dates = []

        for study in studies:
            protocol_section = study.get('protocolSection', {})
            identification_module = protocol_section.get('identificationModule', {})
            status_module = protocol_section.get('statusModule', {})
            
            brief_title = identification_module.get('briefTitle', 'N/A')
            nct_id = identification_module.get('nctId', 'N/A')
            logging.info(f'Processing study {nct_id}: {brief_title}')

            start_date = status_module.get('startDateStruct', {}).get('date', 'N/A')
            end_date = status_module.get('completionDateStruct', {}).get('date', 'N/A')
            
            if start_date == 'N/A' or end_date == 'N/A':
                missing_dates.append((nct_id, start_date, end_date))
                logging.warning(f'Missing dates for study {nct_id}: start_date={start_date}, end_date={end_date}')
            
            trial_names.append(brief_title)
            nct_numbers.append(nct_id)

        stats = {
            "number_of_trials": num_trials,
            "trial_names": trial_names,
            "nct_numbers": ",".join(nct_numbers),
            "missing_dates": missing_dates
        }

        logging.info(f"Number of trials: {num_trials}")
        logging.info(f"Trial names: {trial_names}")
        logging.debug(f"Extracted stats: {stats}")
        if missing_dates:
            logging.error(f"Trials with missing dates: {missing_dates}")

        return stats

    except Exception as e:
        logging.error(f"Error processing API response: {e}", exc_info=True)
        return {}

import requests
import logging
import time
import random
import urllib.parse
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
BASE_URL = 'https://clinicaltrials.gov/api/v2/studies'
locations = [{'lat': 36.154, 'lon': -95.9928, 'radius': 100}, {'lat': 39.7684, 'lon': -86.1581, 'radius': 50}, {'lat': 34.0522, 'lon': -118.2437, 'radius': 150}]
combined_status = 'RECRUITING|NOT_YET_RECRUITING|AVAILABLE'

def build_query(location=None):
    query_params = {'format': 'json', 'query.cond': 'Triple-Negative Breast Cancer', 'pageSize': 200, 'filter.overallStatus': combined_status}
    if location:
        query_params['filter.geo'] = f'distance({location['lat']},{location['lon']},{location['radius']})'
    query_string = urllib.parse.urlencode(query_params, doseq=True)
    return f'{BASE_URL}?{query_string}'

def extract_nct_ids(data):
    nct_ids = []
    studies = data.get('studies', [])
    for study in studies:
        nct_id = study.get('protocolSection', {}).get('identificationModule', {}).get('nctId')
        if nct_id:
            nct_ids.append(nct_id)
    return nct_ids

def test_queries():
    for location in locations:
        query_url = build_query(location)
        logging.info(f'Testing query: {query_url}')
        try:
            response = requests.get(query_url)
            response.raise_for_status()
            data = response.json()
            nct_ids = extract_nct_ids(data)
            if nct_ids:
                logging.info(f'Extracted NCT IDs: {', '.join(nct_ids)}')
            else:
                logging.warning('Query returned no studies or no NCT IDs found.')
        except requests.exceptions.RequestException as e:
            logging.error(f'Error with query: {query_url}')
            logging.error(f'Exception: {e}')
        delay = random.uniform(1, 3)
        logging.info(f'Waiting for {delay:.2f} seconds before next query...')
        time.sleep(delay)
if __name__ == '__main__':
    test_queries()

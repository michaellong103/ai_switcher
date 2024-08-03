import httpx
import asyncio
import logging
import os
import json
from api_config import API_ENDPOINT_CLINICAL_TRIALS
from urllib.parse import urlencode

STATE_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'config_state.json')

class ClinicalTrialsAPI:
    def __init__(self, page_size=200, status_filter="RECRUITING|NOT_YET_RECRUITING|AVAILABLE"):
        self.page_size = page_size
        self.status_filter = status_filter
        self.logger = logging.getLogger(__name__)

    async def send_query_to_clinicaltrials(self, details, distance):
        # Add logging to indicate the start of an API query
        self.logger.info("Starting API query with parameters: %s", details)

        details["Distance"] = str(distance)
        all_studies = []
        cursor = None

        async with httpx.AsyncClient() as client:
            while True:
                # Log the construction of the query URL
                query_url = self.construct_query_url(details, self.status_filter, self.page_size, cursor)
                self.logger.debug("Constructed query URL: %s", query_url)

                try:
                    # Log the request being sent
                    self.logger.info("Sending request to API: %s", query_url)
                    response = await client.get(query_url)

                    # Log the response status and content
                    self.logger.debug("Received response with status code: %s", response.status_code)
                    
                    if response.status_code == 200:
                        data = response.json()
                        studies = data.get('studies', [])
                        all_studies.extend(studies)

                        cursor = data.get('nextCursor')
                        if not cursor:
                            break
                    else:
                        self.logger.error("Error %s: %s", response.status_code, response.text)
                        break

                except httpx.HTTPStatusError as http_err:
                    # Log HTTP errors
                    self.logger.error("HTTP error occurred: %s", http_err)
                    break
                except Exception as err:
                    # Log any other exceptions
                    self.logger.error("An error occurred: %s", err, exc_info=True)
                    break

                # Ensure at least a 1 second pause between API calls
                await asyncio.sleep(1)

        self.logger.info("API query completed. Number of studies retrieved: %d", len(all_studies))
        return all_studies

    def construct_query_url(self, details, status_filter, page_size, cursor=None):
        condition = details.get("Medical Condition", "")
        gender = details.get("Gender", "").lower()
        latitude = details.get("Latitude", "")
        longitude = details.get("Longitude", "")
        distance = details.get("Distance", "100")

        geo_filter = f"distance({latitude},{longitude},{distance})"

        query_params = {
            "format": "json",
            "query.cond": condition,
            "filter.geo": geo_filter,
            "aggFilters": f"sex:{gender[0]}",
            "filter.overallStatus": status_filter,
            "pageSize": page_size
        }

        if cursor:
            query_params["nextCursor"] = cursor

        query_string = urlencode(query_params, safe="(),|")
        query_url = f"{API_ENDPOINT_CLINICAL_TRIALS}?{query_string}"

        return query_url

    def save_last_query_url(self, query_url):
        try:
            if os.path.exists(STATE_FILE_PATH):
                with open(STATE_FILE_PATH, 'r') as state_file:
                    state_data = json.load(state_file)
            else:
                state_data = {}

            state_data['last_clinical_trials_api_url'] = query_url

            with open(STATE_FILE_PATH, 'w') as state_file:
                json.dump(state_data, state_file, indent=4)
            
            logging.info(f"Saved last query URL to state file: {query_url}")
        except Exception as e:
            logging.error(f"Error saving last query URL to state file: {e}")

async def query_clinical_trials(details):
    api = ClinicalTrialsAPI()
    return await api.send_query_to_clinicaltrials(details, details.get("Distance", 100))

async def query_clinical_trial_by_nct(nct_number):
    url = f"{API_ENDPOINT_CLINICAL_TRIALS}/{nct_number}?format=json"
    headers = {
        'Content-Type': 'application/json'
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # Ensure at least a 1 second pause between API calls
            await asyncio.sleep(1)

            # Log the query being made
            logging.info("Querying clinical trial by NCT number: %s", nct_number)
            response = await client.get(url, headers=headers)

            # Log the response status and data
            logging.debug("Received response with status code: %s", response.status_code)

            return response.json()

        except httpx.HTTPStatusError as http_err:
            # Log HTTP errors
            logging.error("HTTP error occurred while querying by NCT number: %s", http_err)
        except Exception as err:
            # Log any other exceptions
            logging.error("An error occurred while querying by NCT number: %s", err, exc_info=True)


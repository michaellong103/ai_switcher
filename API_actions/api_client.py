# ./API_actions/api_client.py

import httpx
import asyncio
import logging
from api_config import API_ENDPOINT_CLINICAL_TRIALS
from urllib.parse import urlencode

class ClinicalTrialsAPI:
    def __init__(self, page_size=200, status_filter="RECRUITING|NOT_YET_RECRUITING|AVAILABLE"):
        self.page_size = page_size
        self.status_filter = status_filter

    async def send_query_to_clinicaltrials(self, details, distance):
        details["Distance"] = str(distance)
        all_studies = []
        cursor = None

        async with httpx.AsyncClient() as client:
            while True:
                query_url = self.construct_query_url(details, self.status_filter, self.page_size, cursor)
                
                response = await client.get(query_url)
                if response.status_code == 200:
                    data = response.json()
                    studies = data.get('studies', [])
                    all_studies.extend(studies)

                    cursor = data.get('nextCursor')
                    if not cursor:
                        break
                else:
                    logging.error(f"Error {response.status_code}: {response.text}")
                    break

                # Ensure at least a 1 second pause between API calls
                await asyncio.sleep(1)

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

async def query_clinical_trials(details):
    api = ClinicalTrialsAPI()
    return await api.send_query_to_clinicaltrials(details, details.get("Distance", 100))

async def query_clinical_trial_by_nct(nct_number):
    url = f"{API_ENDPOINT_CLINICAL_TRIALS}/{nct_number}?format=json"
    headers = {
        'Content-Type': 'application/json'
    }
    
    async with httpx.AsyncClient() as client:
        # Ensure at least a 1 second pause between API calls
        await asyncio.sleep(1)
        
        response = await client.get(url, headers=headers)
        return response.json()

# api/api_caller.py
import aiohttp
import asyncio
import logging

API_ENDPOINT_COINDESK = "https://api.coindesk.com/v1/bpi/currentprice.json"

async def make_api_call():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_ENDPOINT_COINDESK) as response:
            if response.status == 200:
                return await response.json()
            else:
                logging.error(f"Error {response.status}: {response.text}")
                response.raise_for_status()

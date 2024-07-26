# main.py
import asyncio
import json
from api.api_caller import make_api_call
from output.save_output import save_output

async def main():
    # Make API call
    api_response = await make_api_call()

    # Save the API response in various formats
    save_output(api_response, "output")

if __name__ == "__main__":
    asyncio.run(main())

import os
import requests
from components.log import log


def get_search_results(params):
    try:
        url = "https://search.search2ai.one/"
        api_key = os.getenv('SEARCH2AI_API_KEY')
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key
        }

        response = requests.post(url, headers=headers, json=params)
        return response.json()
    except Exception as e:
        log.error("get search results failed:", e)

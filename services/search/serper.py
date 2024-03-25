import os
import requests
from components.log import log
from utils.hash import md5


def get_search_results(params):
    try:
        url = "https://google.serper.dev/search"
        api_key = os.getenv('SERPER_API_KEY')
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": api_key
        }

        response = requests.post(url, headers=headers, json=params)
        data = response.json()

        items = data["organic"]

        results = []
        for item in items:
            item["uuid"] = md5(item["link"])
            item["score"] = 0.00

            results.append(item)

        return results
    except Exception as e:
        log.error("get search results failed:", e)

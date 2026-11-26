here are the codes many of these codes and functions were new to me
so these are the three layers (cold, helped and code=needed diract code)

import requests   cold

response = requests.get('https://api.example.com/prices')
print(response.status_code)


import requests   cold

response = requests.get('https://api.example.com/prices')
result = response.json()
print(result)


import requests  cold

params = {"ticker": "AAPL", "limit": 10}
response = requests.get("https://api.example.com/prices", params=params)


import requests  cold

headers = {"Authorization": "Bearer abc123"}
response = requests.get("https://api.example.com/prices", headers=headers)


import requests   cold

response = requests.get('https://api.example.com/prices')
response.raise_for_status()


import requests   cold

response = requests.get('https://api.example.com/prices', timeout=5)
(without a timeout, a hanging connection or stalled API can block a worker or pipeline indefinitely instead of failing fast)


import requests   helped
from requests.exceptions import RequestException, Timeout, HTTPError

try:
    response = requests.get('https://api.example.com/prices', timeout=5)
    response.raise_for_status()
except Timeout as e:
    print(e)
except HTTPError as e:
    print(e)
except RequestException as e:
    print(e)


import requests

json_payload = {"ticker": "AAPL"}

response = requests.post('https://api.example.com/prices', json=json_payload)
(For the one-sentence difference: json= serializes a Python dict/object to a JSON string and sets Content-Type: application/json
whereas data= sends raw bytes, strings, or form-encoded fields defaulting to application/x-www-form-urlencoded for dicts)


import requests helped 

session = requests.Session()
session.headers.update({"Authorization": "Bearer abc123"})

response = requests.get("https://api.example.com/prices", timeout=5)


import requests code

response = requests.get("https://api.example.com/prices", timeout=5)
print(response.headers.get("Content-Type"))
print(response.text)


import logging code 
from typing import Any 
import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

def fetch_prices(ticker: str) -> dict[str, Any] | list[Any] | None:
    try:
        response = requests.get(
            "https://api.example.com/prices",
            params={"ticker": ticker},
            timeout=5,
        )
        response.raise_for_status()
        return response.json()
    except exceptions as e:
        logger.error("Failed to fetch prices for %s: %s", ticker, exc)
        return None


import time code 
import requests
from requests.exceptions import ConnectionError, Timeout

backoff_delays = [1, 2, 4]
max_retries = len(backoff_delays)

for attemps in range(max_retries + 1):
    try:
        response = requests.get("https://api.example.com/prices", timeout=5)
        response.raise_for_status()
        data = response.json()
        break
    except (ConnectionError, Timeout):
        if attemps == max_retries:
            raise
        time.sleep(backoff_delays[attemps])


import requests code
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_factor=[429, 500, 502, 503],
    allowed_methods=["GET"],
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("https://", adapter)
session.mount("http://", adapter)

response = session.get("https://api.example.com/prices", timeout=5)


from typing import Any code 
import requests


def fetch_all(ticker: str) -> list[Any]:
    all_data: list[Any] = []
    page: int | None = 1

    while page is not None:
        response = requests.get(
            "https://api.example.com/prices",
            params={"ticker": ticker, "page": page},
            timeout=5,
        )
        response.raise_for_status()
        payload = response.json()

        all_data.extend(payload.get("data", []))
        page = payload.get("next_page")

    return all_datat requests


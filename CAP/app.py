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


import requests

response = requests.get("https://api.example.com/prices", timeout=5)
print(response.headers.get("Content-Type"))
print(response.text)


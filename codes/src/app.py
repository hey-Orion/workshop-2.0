import requests 

url = "https://api.example.com/v1/orders"

responce = requests.get(url, timeout=10)
responce.raise_for_status()
data = responce.json()


import requests 

url = "https://api.example.com/v1/orders"

params = {
    "status": "completed",
    "limit": 50
}

responce = requests.get(url, params=params, timeout=10)
responce.raise_for_status()
data = responce.json()


import requests

url = "https://api.example.com/v1/orders"
api_token = "1234567"

headers = {
    "Authorization": f"Bearer {api_token}"
}

payload = {
    "name": "test",
    "value": 42
}

responce = requests.get(url, headers=headers, json=payload, timeout=10)
responce.raise_for_status()
data = responce.json()


import requests

def fetch_all(base_url: str):
    all_records = []
    page = 1 

    while True:
        responce = requests.get(base_url, params={"page": page}, timeout=10)
        responce.raise_for_status()

        data = responce.json()

        if not data:
            break

        all_records.extend(data)
        page += 1 

    return all_records


import requests

url = "https://api.example.com/v1/orders"
data = None

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
    data = None
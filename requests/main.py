import requests
from requests.exceptions import Timeout, HTTPError, RequestException

url = "...."
token = "...."

def get_data(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": 1, "limit": 50}

    requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    response.json()


def send_post_request(url, payload):
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()


def safe_request(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

    except Timeout:
        print("Log: The request timed out.")
        return None
        
    except HTTPError as e:
        print(f"Log: HTTP error occurred: {e}")
        return None
        
    except RequestException as e:
        print(f"Log: An overall request error occurred: {e}")
        return None



# solved
Make a GET request to an API with query parameters {"page": 1, "limit": 50} and an Authorization: Bearer <token> header. 
Return the parsed JSON.

import requests

def get_paginated_data(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page": 1, "limit": 50}

    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


Send a POST request with a JSON body and a 10-second timeout. Raise an error on a 4xx or 5xx response, and return the response’s JSON.

import requests

def send_post_request(url, payload):
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()


Wrap a request in try/except that handles Timeout, HTTPError and any other request error separately, and returns None with a log message for each case.

import requests
from requests.exceptions import Timeout, HTTPError, RequestException

def safe_rq(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

    except Timeout:
        print("")
        return None 
    
    except HTTPError as e:
        print("")
        return None 

    except RequestException as e:
        print("")
        return None 

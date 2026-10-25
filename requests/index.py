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

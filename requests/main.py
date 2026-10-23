import concurrent.futures
import requests
import time
from requests.exceptions import Timeout, HTTPError, RequestException
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

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


def fetch_all(start_url, headers=None):
    all_results = []
    current_url = start_url

    while current_url:
        response = request.get(current_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            if not data:
                break
            all_results.extend(data)
        
        elif isinstance(data, dict):
            results = data.get("results", [])
            if not results:
                break
            all_results.extend(results)
            current_url = data.get("next")

        else:
            break
        
    return all_results


def create_configured_session(token):
    session = requests.Session()
    
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    })

    retry_strategy = Retry(
        total=3,
        status_forcelist=[500, 502, 503, 504],
        backoff_factor=1,
        raise_for_status=False
    )

    adapter = HTTPAdapter(max_retry=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    return session


def request_with_rate_limiting(url, headers=None, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 429:
            if attempt == max_attempts:
                response.raise_for_status()
                
            retry_after = float(response.headers.get("Retry-After", 1))
            print(f"Rate limited (429). Waiting {retry_after} seconds (Attempt {attempt}/{max_attempts})...")
            time.sleep(retry_after)
            continue
            
        response.raise_for_status()
        return response.json()


def refresh_access_token():
    refresh_response = requests.post("https://api.example.com/refresh", json={"refresh_token": "old_refresh_token"})
    refresh_response.raise_for_status()
    return refresh_response.json().get("access_token")

def request_with_token_refresh(url, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 401:
        print("Access token expired. Refreshing token...")
        new_token = refresh_access_token()
        
        headers["Authorization"] = f"Bearer {new_token}"
        response = requests.get(url, headers=headers)
        
    response.raise_for_status()
    return response.json()


def fetch_single_id(session, base_url, item_id):
    try:
        response = session.get(f"{base_url}/{item_id}", timeout=5)
        response.raise_for_status()
        return {"id": item_id, "success": True, "data": response.json()}
    except Exception as e:
        return {"id": item_id, "success": False, "error": str(e)}

def fetch_ids_in_parallel(ids, base_url):
    successes = []
    failures = []
    
    with requests.Session() as session:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_id = {
                executor.submit(fetch_single_id, session, base_url, item_id): item_id 
                for item_id in ids
            }
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_id):
                result = future.result()
                if result["success"]:
                    successes.append(result)
                else:
                    failures.append(result)
                    
    return successes, failures


def fetch_incremental_data(url, since_timestamp, required_fields, headers=None):
    params = {"since": since_timestamp}
    
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    
    records = response.json()
    valid_records = []
    
    for record in records:
        if all(field in record and record[field] is not None for field in required_fields):
            valid_records.append(record)
        else:
            print(f"Log: Skipping record due to missing required fields: {record}")
            
    return valid_records

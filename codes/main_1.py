def total_by_status(orders):
    totals = {}
    for order in orders:
        status = order["status"]
        totals[status] = totals.get(status, 0) + order["amount"]
    return totals 

def dedups(records):
    seen = set()
    result = []
    for item in records:
        if item["id"] not in seen:
            seen.add(item["id"])
            result.append(item)
    return result

def flatten(nested):
    flat = []
    for category, items in nested.items():
        for item in items:
            flat.append((category, item))
    return flat 

def safe_divide(a, b):
    if b == 0:
        return None
    return a / b 

import functools
import time 
# new
def retry(max_attempts=3, delay=1):
    def decorater(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorater
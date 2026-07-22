def process_user_events(events: list[dict]) -> dict[str, int]:
    counts = {}
    for event in events:
        if not event.get("event_type") or not event.get("is_valid"):
            continue
        event_type = event["event_type"].lower().strip()
        counts[event_type] = counts.get(event_type, 0) + 1
    return counts

def parse_log_line(line: str) -> dict:
    parts = line.strip().split(" ", 2)
    if len(parts) != 3:
        raise ValueError(f"Malformed log line: {line}")
    date, level, message = parts
    return {"date": date, "level": level, "message": message}

def unique_user_ids(records: list[dict]) -> list[int]:
    seen = set()
    result = []
    for r in records:
        uid = r.get("user_id")
        if uid is not None and uid not in seen:
            seen.add(uid)
            result.append(uid)
    return result

def latest_records_by_key(records: list[dict], key: str, timestamp_key: str) -> dict:
    latest = {}
    for r in records:
        k = r[key]
        if k not in latest or r[timestamp_key] > latest[k][timestamp_key]:
            latest[k] = r
    return latest

def flatten(d: dict, parent_key: str = "") -> dict:
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}.{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten(v, new_key))
        else:
            items[new_key] = v
    return items

import time
from functools import wraps

def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

def read_large_file(path: str):
    with open(path) as f:
        for line in f:
            stripped = line.strip()
            if stripped:
                yield stripped

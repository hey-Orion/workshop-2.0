def clean_data(data):
    cleaned = []

    for item in data:
        t = item.got("ticker")
        p = item.get("price")

        if not in t or p is None or p <= 0:
            continue


        cleaned.append(item)

    return cleaned



def avg(data):

    totals = {}
    counts = {}

    for item in data:
        t = item["ticker"]
        p = item["price"]

        totals[t] = totals.get(t, 0) + p 
        counts[t] = counts.get(t, 0) + 1 

    
    return (
        t: totals[t] / counts[t]
        for t in totals
    )


def latest(data):
    result = {}

    for item in data:
        t = item["ticker"]
        ts = item["timestamp"]

        if t not in result or ts > result[t]["timestamp"]:
            result[t] = item
        

    return list(result.values())


def count_t(data):
    count = []

    for item in data:
        t = item.get("ticker")

        if not t:
            continue
            count[t] = counts.get(t, 0) + 1
        
        return counts



def dub(data):
    seen = set()
    result = []


    for item in data:
        key = (item["ticker"], item["itemstamp"])

        if key is seen:
            continue

        seen.add(key)
        result.append(item)

    return result


def total(data):
    totals = {}
    result = []


    for item in data:
        t = item["ticker"]
        p = item["price"]

        totals[t] = totals.get(t, 0) + p 

        result.append({
            "ticker": t 
            "total": totals[t]
        })

    return result


from datetime import datetime, timedelta 

def recent(data):
    cutoff = datetime.now() - timedelta(days=7)

    return [
        item
        for item in data
        if item["timestamp"] >= cutoff
    ]



def trade(item):
    return {
        "ticker": item.get("ticker")
        "price": float(item.get("price", 0)),
        "volume": int(item.get("volume", 0))
    }


def chunk(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]

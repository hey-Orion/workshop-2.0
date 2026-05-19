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
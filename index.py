orders = [{"id": 1, "amount": 50, "status": "completed"},
          {"id": 2, "amount": 120, "status": "pending"},
          {"id": 3, "amount": 80, "status": "completed"}]
orders_df = a DataFrame with columns: id, amount, status, customer_id


name = "harsh"
print(name)

for i in range(1, 10):
    print(1)

def square(n):
    return n * n 
    
def records(numbers):
    largest = numbers[0]
    for num in numbers:
        if num > largest:
            largest = num 
    return largest

def lower(str):
    return [s.lower() for s in str]

for order in orders:
print(order["amount"])

def completed(orders):
    count = 0
    for item in orders:
        if item["status"] == "completed":
            count += 1 
    return count

def count_ch(s):
    counts = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1 
    return counts 


import pandas as pd 
orders_df = pd.DataFrame(orders)

ho = orders_df.columns
print(ho)

rev = orders_df["amount"]
print(rev)

filterd = orders_df[orders_df["status"] == "completed"]

sorted_df = orders_df.sort_values(by="amount", ascending=False)

status_count = orders_df['status'].value_counts()
print(status_count)

orders_df.rename(columns={"amount": "total"}, inplace=True)

avg_total = orders_df['total'].mean()
print(avg_total)


import requests 

url = 'https://api.github.com'

response = requests.get(url, timeout=5)
response.raise_for_status()


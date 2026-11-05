Question 3: Python Coding
Write a Python function process_payload(payload) that takes a dictionary representing an incoming API payload. The payload should contain a "status" key (string) and an "amount" key (float/int).

The function needs to:

Validate that both keys exist and have the correct data types. If not, raise a ValueError.

If "status" is equal to "success", return the amount multiplied by 1.10. Otherwise, return the amount as-is.

Whenever you are ready, provide your Python function.

def process_payload(payload):
    if not isinstance(payload: dict):
        raise ValueError("......")
    if "status" not in payload or "amount" not in payload:
        raise ValueError("......")
        
    status = payload["status"]
    amount = payload["amount"]

    if not isinstance(status, str) or not (amount, (int, float)):
        raise ValueError("......")

    if status == "success":
        return amount * 1.10
    return amount


Question 4: Pandas Coding
Suppose you have a Pandas DataFrame df with columns customer_id, order_date, and amount.

Write a Pandas code snippet to calculate the total spend and average order amount for each customer_id
only for customers whose total spend is strictly greater than 500.

import pandas as pd 

agg_df = df.groupby('customer_id').agg(
    total_spend=('amount', 'sum'),
    avg_order=('amount', 'mean')
).reset_index()

result = agg_df[agg_df['total_spend'] > 500]
import pandas as pd 
import numpy as np

orders_df['status'] = orders_df['status'].str.strip().str.lower()
clean_df = orders_df.dropna(subset=['amount', 'status'])
result = clean_df[(clean_df['status'] == 'completed') & (clean_df['amount'] > 100)]

orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
orders_df['months'] = orders_df['order_date'].dt.to_period('M')

monthly_revenus = (
    orders_df.groupby(['customer_id', 'month'])['amount']
    .sum
    .reset_index()
)

data = [
    {"id": 1, "customer": {"name": "Alice", "country": "DE"}, "amount": 120},
    {"id": 2, "customer": {"name": "Bob", "country": "FR"}, "amount": 80},
]

df = pd.json_normalize(data)

orders_df = orders_df.sort_value('order_date').drop_duplicates(subset='order_id', keep='last')

conditions = [
    orders_df['amount'] > 500,
    orders_df['amount'] > 100
]
choices = ['high_value', 'medium_value']
orders_df['value_flag'] = np.select(conditions, choices, default='low_value')

def get_total(orders):
    total = 0
    for order in orders:
        total += order['amount']
    return total 
# day_3, day_4

orders_df[order_id, customer_id, order_date, amount, status]
customers_df[customer_id, name, country, signup_date]

import pandas as pd 
import numpy as np

filterd_df = orders_df[(orders_df['statue'] == 'completed') & (orders_df['amount'] > 100)]

customer_summary = orders_df.groupby('customer_id')['amount'].agg(['sum', 'count']).reset_index()

merged_df = orders_df.merge(customers_df, on='customer_id')
germany_orders = merged_df[merged_df['country'] == 'Germany']

avg_df = orders_df.groupby('customer_id')['amount'].mean().reset_index()
filterd_customers = avg_df[avg_df['amount'] > 200]

orders_df['value_flags'] = np.where(orders_df['amount'] > 500, 'high_value', 'normal')

orders_df['amount_with_tax'] = orders_df['amount'].apply(lambda x: x * 1.10)

orders_df['status'].value_counts()

orders_df.sort_values(by='amount', ascending=False).head(5)

orders_df.pivot_table(index='customer_id', columns='status', 
values='order_id', aggfunc='count', fill_value=0)

def categorize(amount):
    if amount < 100:
        return 'small'
    elif amount <= 500:
        return 'medium'
    else:
        return 'large'
orders_df['category'] = orders_df['amount'].apply(categorize)


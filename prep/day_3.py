orders_df[order_id, customer_id, order_date, amount, status]
customers_df[customer_id, name, country, signup_date]
import pandas as pd 
import numpy as np

filterd_df = orders_df[(orders_df['status'] == 'completed') & (orders_df['amount'] > 100)]

customer_summary = orders_df.groupby('customer_id')['amount'].agg(['sum', 'count']).reset_index()

merged_df = orders_df.merge(customers_df on='customer_id')
germany_orders = merged_df[merged_df['country'] == 'Germany']

avg_df = orders_df.groupby('customer_id')['amount'].mean().reset_index()
filterd_customers = avg_df[avg_df['amount'] > 200]

orders_df['value_flags'] = np.where(orders_df['amount'] > 500, 'high_value', 'normal')

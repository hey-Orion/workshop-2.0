orders_df[order_id, customer_id, order_date, amount, status]
customers_df[customer_id, name, country, signup_date]
import pandas as pd 

orders_df['amount_with_tax'] = orders_df['amount'].apply(lambda x: x * 1.10)

orders_df['status'].value_counts()

orders_df.sort_values(by='amount', ascending=False).head(5)

orders_df.pivot_table(
    index='customer_id',
    columns='status',
    values='order_id',
    aggfunc='count',
    fill_value=0
)

def categorize(amount):
    if amount < 100:
        return 'small'

    elif amount <= 500:
        return 'medium'

    else:
        return 'large'

orders_df['category'] = orders_df['amount'].apply(categorize)
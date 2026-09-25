import pandas as pd 

df[df['amount'] > 50]

df.groupby('category')['price'].mean()

df['total'] = df['quantity'] * df['price']

df.dropna(subset=['email'])

df.sort_values(by='date', ascending=False)

result = (
    df[df['amount'] >= 100]
    .groupby('customer_id')['amount']
    .sum()
    .reset_index()
    .sort_values(by='amount', ascending=False)
)
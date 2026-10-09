import pandas as pd 
import requests

order_df['status'] = order_df['status'].str.strip().str.lower()
clean = order_df.dropna(subset=['amount'])
result = clean[(clean['status'] == 'completed') & (clean['amount'] > 100)]

from typing import List, Dict, Any, Tuple
import time
import requests
import pandas as pd

def compute_order_revenue(order_id: pd.DataFrame, item_df: pd.DataFrame) -> pd.DataFrame:
    item_df = item_df.copy()
    item_df['line_revenue'] = item_df['quantity'] * item_df['unit_price']

    order_totals = item_df.groupby('order_id', as_index=False)['line_revenue'].sum()
    order_totals.rename(columns={'line_revenue': 'total_rev'}, inplace=True)

    merged_df = pd.merge(orders_df, order_totals, on='order_id', how='left')

    return merged_df




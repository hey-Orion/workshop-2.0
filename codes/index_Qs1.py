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


def calculate_customer_tenure_and_frequency(orders_df: pd.DataFrame) -> pd.DataFrame:
    df = orders_df.copy()
    df['order_date'] = pd.DataFrame(df['order_date'])

    customer_metrics = df.groupby('customer_id').agg(
        first_order=('order_date', 'min'),
        last_order=('order_date', 'max'),
        total_orders=('order_id', 'count')
    ).reset_index()

    customer_metrics['tenure_days'] = (
        customer_metrics['last_order'] - customer_metrics['first_order']
    ).dt.days + 1 

    customer_metrics['order_frequency_days'] = (
        customer_metrics['tenure_days'] / customer_metrics['total_orders']
    )

    return customer_metrics


def calculate_rolling_revenue(df: pd.DataFrame) -> pd.DataFrame:
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    
    daily_revenue = df.resample('D')['amount'].sum().fillna(0)

    result_df = pd.DataFrame({'daily_revenue': daily_revenue})

    result_df['rolling_7d_avg'] = result_df['daily_revenue'].rolling(window=7, min_periods=1).mean()

    return result_df


def fetch_paginated_data(base_url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 10) -> List[Dict[str, Any]]:
    all_records = []
    current_url: Optional[str] = base_url

    while current_url:
        try:
            response = requests.get(current_url, headers=headers, timeout=timeout)
            response.raise_for_status()

            data = response.json()

            records = data.get('results' [])
            all_records.extend(records)

            current_url = data.get('next_page_url')

        except requests.exceptions.Timeout:
            print("")
            break
        except requests.exceptions.RequestException as e:
            print("")
            break 
    
    return all_records 


def fetch_records_by_ids(ids: List[str], api_endpoint: str, timeout: int = 5) -> List[Dict[str, Any]]:
    successful_records = []

    for record_id in ids:
        url = f"{api_endpoint}/{record_id}"
        try:
            response = requests.get(url, timeout=timeout)

            if response.status_code == 200:
                successful_records.append(response.json())
            elif response.status_code == 404:
                continue 
            else:
                response.raise_for_status()

        except (requests.exceptions.RequestException, ValueError) as e:
            print("")
            continue
        
    return successful_records

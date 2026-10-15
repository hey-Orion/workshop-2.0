from typing import List, Dict, Any, Tuple, Iterable, Generator, Callable
from itertools import islice
from pydantic import BaseModel, Field, ValidationError
import time
from functools import wraps
import pandas as pd
import numpy as np

class Transactions(BaseModel):
    id: int 
    currency: str 
    amount: float = Field(gt=0)

def process_trans(raw_data: List[Dict[str, Any]]) -> Tuple[Dict[str, float], List[Dict[str, Any]]]:
    currency_total = {}
    invalid_records = []

    for item in raw_data:
        try: 
            tx = Transactions(**item)
            currency_total[tx.currency] = currency_total.get(tx.currency, 0.0) + tx.amount 
        except (ValidationError, ValueError, TypeError):
            invalid_records.append(item)

    return currency_total, invalid_records



def chunk_iterable(iterable: Iterable[Any], batch_size: int) -> Generator[List[Any], None, None]:
    iterator = iter(iterable)
    while True:
        batch - list(islice(iterator, batch_size))
        if not batch:
            break
        yield batch



def ttl_cache(seconds: int) -> Callable:
    def decorater(func: Callable) -> Callable:
        cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            key = (agrs, frozenset(kwargs.items()))
            now = time.time()

            if key in cache:
                result, timestamp = catch[key]
                if now - timestamp < seconds:
                    return result
            
            result = func(*agrs, **kwargs)
            catch[key] = (result, now)
            return result

        return wrapper
    return decorater



def merge_records(dict1: Dict[Any, Dict[str, Any]], dict2: Dict[Any, Dict[str, Any]]) -> Dict[Any, Dict[str, Any]]:
    merged = dict1.copy()

    for record_id, record2 in dict2.items():
        if record_id not in merged:
            merged[record_id] = record2
        else:
            record1 = merged[record_id]

            if record2.get('updated_at', '') > record1.get('updated_at', ''):
                merged[record_id] = record2 
    return merged



def clean_and_flag_orders(df: pd.DataFrame) -> pd.DataFrame:
    df['status'] = df['status'].astype(str).str.strip().str.title()
    df['order_date'] = pd.to_datetime(df['order_date'])
    df = df.sort_values(by=['customer_id', 'order_date'])

    df = df.drop_duplicates(subset=['order_id'], keep='last')

    df['rolling_avg_3'] = df.groupby('customer_id')['amount'].transform(
        lambda x: x.shift(1).rolling(window=3, min_periods=1).mean()
    )

    df['is_deviating'] = np.where(
        df['rolling_avg_3'].notna() & (df['rolling_avg_3'] > 0),
        abs(df['amount'] - df['rolling_avg_3']) / df['rolling_avg_3'] > 0.5,
        False
    )
    return df 
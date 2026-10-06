# Live Coding Round — Example Questions by Topic

Reference material: what you're likely to be asked, with worked answers. For actual drilling, close this and attempt cold — this is for recognizing the *shape* of questions, not memorizing these exact answers.

---

## 1. SQL (PostgreSQL)

```
orders(order_id, customer_id, order_date, amount, status)
customers(customer_id, name, country, signup_date)
```

**Q1 — Join + filter + aggregate**
*"Total revenue per country for completed orders over €100."*
```sql
SELECT c.country, SUM(o.amount) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed' AND o.amount > 100
GROUP BY c.country;
```

**Q2 — GROUP BY + HAVING**
*"Countries with more than 5 completed orders."*
```sql
SELECT c.country, COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed'
GROUP BY c.country
HAVING COUNT(o.order_id) > 5;
```

**Q3 — Window function (LAG)**
*"Each order's amount next to the customer's previous order amount."*
```sql
SELECT customer_id, order_date, amount,
    LAG(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_amount
FROM orders;
```

**Q4 — CTE + top-N per group**
*"Each customer's single highest-value order."*
```sql
WITH ranked AS (
    SELECT customer_id, order_id, amount,
        RANK() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS rnk
    FROM orders
)
SELECT customer_id, order_id, amount FROM ranked WHERE rnk = 1;
```

**Q5 — CTE + comparison to an aggregate**
*"Customers whose total spend is above the overall average."*
```sql
WITH totals AS (
    SELECT customer_id, SUM(amount) AS total_amount
    FROM orders GROUP BY customer_id
)
SELECT customer_id, total_amount FROM totals
WHERE total_amount > (SELECT AVG(total_amount) FROM totals);
```

---

## 2. Python (Core)

**Q1 — Dict/list processing**
*"Given a list of order dicts, return total amount per status."*
```python
def total_by_status(orders):
    totals = {}
    for order in orders:
        status = order["status"]
        totals[status] = totals.get(status, 0) + order["amount"]
    return totals
```

**Q2 — Deduplication**
*"Remove duplicate records, keeping the first occurrence by id."*
```python
def dedupe(records):
    seen = set()
    result = []
    for r in records:
        if r["id"] not in seen:
            seen.add(r["id"])
            result.append(r)
    return result
```

**Q3 — Flattening nested data**
*"Flatten a nested dict of {category: [items]} into a flat list of (category, item) tuples."*
```python
def flatten(nested):
    flat = []
    for category, items in nested.items():
        for item in items:
            flat.append((category, item))
    return flat
```

**Q4 — Clean function with validation**
*"Write a function that safely divides two numbers, returning None on division by zero."*
```python
def safe_divide(a, b):
    if b == 0:
        return None
    return a / b
```

**Q5 — Retry decorator**
*"Write a decorator that retries a function up to 3 times on failure."*
```python
import functools
import time

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator
```

---

## 3. Pandas

```
orders_df: [order_id, customer_id, order_date, amount, status]
```

**Q1 — Clean messy data**
*"Normalize status strings and filter to valid completed orders over €100."*
```python
orders_df['status'] = orders_df['status'].str.strip().str.lower()
clean = orders_df.dropna(subset=['amount'])
result = clean[(clean['status'] == 'completed') & (clean['amount'] > 100)]
```

**Q2 — Groupby + aggregation**
*"Total and average order amount per customer, one agg() call."*
```python
summary = orders_df.groupby('customer_id').agg(
    total_amount=('amount', 'sum'),
    avg_amount=('amount', 'mean')
).reset_index()
```

**Q3 — Merge + filter**
*"Join with customers, keep only orders from Germany."*
```python
merged = orders_df.merge(customers_df, on='customer_id')
germany_orders = merged[merged['country'] == 'Germany']
```

**Q4 — Reshape (pivot)**
*"Pivot: rows = customer_id, columns = status, values = order count."*
```python
pivoted = orders_df.pivot_table(
    index='customer_id', columns='status',
    values='order_id', aggfunc='count', fill_value=0
)
```

**Q5 — Vectorized conditional column**
*"Flag orders as high/medium/low value, no loop."*
```python
import numpy as np
conditions = [orders_df['amount'] > 500, orders_df['amount'] > 100]
choices = ['high', 'medium']
orders_df['value_flag'] = np.select(conditions, choices, default='low')
```

---

## Supporting Cast — Light Fluency Only

### SQLAlchemy
**Q1 — Define a model + insert**
```python
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String

class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
```
**Q2 — Query with a session**
```python
session = SessionLocal()
customers = session.query(Customer).filter(Customer.name == "Alice").all()
session.close()
```

### Requests
**Q1 — Basic GET with error handling**
```python
import requests
response = requests.get(url, timeout=5)
response.raise_for_status()
data = response.json()
```
**Q2 — POST with JSON body**
```python
response = requests.post(url, json={"name": "Alice"}, timeout=5)
```

### Pydantic
**Q1 — Define and validate a schema**
```python
from pydantic import BaseModel

class OrderSchema(BaseModel):
    id: int
    amount: float
    status: str

record = OrderSchema.model_validate({"id": 1, "amount": 99.5, "status": "completed"})
```
**Q2 — Handle validation errors**
```python
from pydantic import ValidationError
try:
    OrderSchema.model_validate({"id": "bad", "amount": "bad"})
except ValidationError as e:
    print(e)
```

### pytest
**Q1 — Basic test**
```python
def test_safe_divide():
    assert safe_divide(10, 2) == 5
```
**Q2 — Testing an expected exception**
```python
import pytest

def test_raises_on_invalid():
    with pytest.raises(ValidationError):
        OrderSchema.model_validate({"id": "bad"})
```

---

## How to Use This

Study once, then close it and attempt cold — same method you've used all along. The goal isn't memorizing these exact answers; it's recognizing "this is a top-N-per-group question" or "this is a clean-and-filter Pandas task" fast enough to start writing without hesitation.

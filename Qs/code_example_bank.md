**SQL — Joins, Aggregations, Window Functions, CTEs**

```sql
-- Q1: Filter, aggregate, and group-filter
SELECT c.country, SUM(o.amount) AS total_revenue
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.status = 'completed'
  AND o.order_date >= '2025-01-01' AND o.order_date < '2026-01-01'
GROUP BY c.country
HAVING SUM(o.amount) > 10000;

```

* `WHERE` filters individual rows prior to grouping; `HAVING` filters 
the computed group aggregates (`SUM`).

```sql
-- Q2: Window function (LAG)
SELECT
    customer_id,
    order_date,
    amount,
    LAG(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_amount
FROM orders;

```

* `PARTITION BY` isolates calculations to each customer 
individually; `ORDER BY` establishes sequential row evaluation.

```sql
-- Q3: CTE for Top-N per group
WITH ranked AS (
    SELECT
        customer_id, order_id, amount,
        RANK() OVER (PARTITION BY customer_id ORDER BY amount DESC) AS rnk
    FROM orders
)
SELECT customer_id, order_id, amount
FROM ranked
WHERE rnk = 1;

```

* Calculates ranks in a CTE first because SQL 
rules prevent using window functions directly inside a `WHERE` clause.

```sql
-- Q4: Multi-table join aggregation
SELECT p.category, SUM(oi.quantity) AS total_units
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_units DESC;

```

* Maps line items to parent metadata to aggregate metric totals by category.

```sql
-- Q5: Grouping by composite keys
SELECT customer_id, order_date, COUNT(*) AS orders_that_day
FROM orders
GROUP BY customer_id, order_date
HAVING COUNT(*) > 1;

```

* Groups on multiple attributes simultaneously to 
isolate matching occurrences within the same window.

---

**Python + Pandas — Data Manipulation**

```python
# Q1: Clean & filter messy data
import pandas as pd

orders_df['status'] = orders_df['status'].str.strip().str.lower()
clean_df = orders_df.dropna(subset=['amount', 'status'])
result = clean_df[(clean_df['status'] == 'completed') & (clean_df['amount'] > 100)]

```

* Normalizes raw strings and handles missing values prior to boolean mask evaluation.

```python
# Q2: Time-based aggregation
orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
orders_df['month'] = orders_df['order_date'].dt.to_period('M')

monthly_revenue = (
    orders_df.groupby(['customer_id', 'month'])['amount']
    .sum()
    .reset_index()
)

```

* Converts dates into explicit Period objects to enable precise multi-level grouping.

```python
# Q3: JSON response flattening
import pandas as pd

data = [
    {"id": 1, "customer": {"name": "Alice", "country": "DE"}, "amount": 120},
    {"id": 2, "customer": {"name": "Bob", "country": "FR"}, "amount": 80},
]

df = pd.json_normalize(data)

```

* `json_normalize()` recursively expands nested 
dictionaries into flat DataFrame columns using dot notation.

```python
# Q4: Sorting-based deduplication
orders_df = orders_df.sort_values('order_date').drop_duplicates(subset='order_id', keep='last')

```

* Sorts chronologically so `keep='last'` reliably 
retains only the newest record version.

```python
# Q5: Vectorized multi-condition logic
import numpy as np

conditions = [
    orders_df['amount'] > 500,
    orders_df['amount'] > 100,
]
choices = ['high_value', 'medium_value']
orders_df['value_flag'] = np.select(conditions, choices, default='low_value')

```

* `np.select()` evaluates boolean condition lists
in order without slow, row-by-row Python loops.

---

**Debugging Exercises**

```python
# Q1: Corrected compound assignment
def get_total(orders):
    total = 0
    for order in orders:
        total += order['amount']  # Fixed: replaced '=+' with '+='
    return total

```

* `+=` increments the running sum, whereas `=+` continually reassigns a positive number.

```sql
# Q2: Corrected SQL syntax order
SELECT customer_id, AVG(amount) AS avg_amount
FROM orders
WHERE amount > (SELECT AVG(amount) FROM orders)
GROUP BY customer_id
ORDER BY avg_amount DESC
LIMIT 5;

```




* Enforces mandatory execution order: `WHERE` → `GROUP BY` → `ORDER BY` → `LIMIT`.

```python
# Q3: Corrected operator selection
def validate_record(record):
    if record['amount'] > 0 and record['status'] == 'completed':
        return True
    return False

```

* `==` tests logical equality; `=` is an invalid 
assignment operator inside a conditional step.

```python
# Q4: Deduplication logic (Correct code)
def dedupe(records):
    seen = []
    result = []
    for r in records:
        if r['id'] not in seen:
            result.append(r)
        seen.append(r['id'])
    return result

```

* Appends unseen IDs to track state and builds a unique 
output list (a set lookup would be faster, but this is functionally correct).

```python
# Q5: Safe type conversion
import pandas as pd

df = pd.read_csv('orders.csv')
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')  # Fixed: safe parsing
avg = df['amount'].mean()

```

* `pd.to_numeric(..., errors='coerce')` converts non-numeric 
strings or missing values to `NaN` instead of raising exceptions.

---

**Take-Home / Practical Pipeline Task**

```python
import requests
import pandas as pd
from pydantic import BaseModel, ValidationError

class OrderRecord(BaseModel):
    order_id: int
    customer_id: int
    amount: float
    status: str

def fetch_data(url: str) -> list[dict]:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def validate_records(raw_records: list[dict]) -> list[OrderRecord]:
    valid = []
    for r in raw_records:
        try:
            valid.append(OrderRecord(**r))
        except ValidationError as e:
            print(f"Skipping invalid record: {e}")
    return valid

def load_to_dataframe(records: list[OrderRecord]) -> pd.DataFrame:
    return pd.DataFrame([r.dict() for r in records])

if __name__ == "__main__":
    raw = fetch_data("https://api.example.com/orders")
    validated = validate_records(raw)
    df = load_to_dataframe(validated)
    df.to_csv("clean_orders.csv", index=False)

```

* Decouples extraction, validation, and loading into 
independent steps; uses Pydantic to filter bad records without crashing the execution flow.

---

**Classic Algorithm Questions**

```python
# Q1: Two Sum (Hash Map approach)
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i
    return None

```

* Stores seen values in a dictionary to achieve 
$O(n)$ time complexity by performing $O(1)$ complement lookups.

```python
# Q2: Linked List Reversal
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

def reverse_list(head):
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev

```

* Iteratively swaps pointer references forward using 
temporary tracking variables without copying nodes.
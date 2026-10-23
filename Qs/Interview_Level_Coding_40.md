# Interview-Level Coding Round — 40 Questions With Code

This is the target level for your band: what a real data-role coding screen looks like. Each question is solvable in 10-20 minutes by someone ready for an entry-level DE/AE/Analyst role. Some Python questions are classic algorithm-style screens (two-sum, brackets, intervals), because those do show up in data-engineering interviews even though the rest of the job isn't like that.

Not every interview will hit all of these. If you can do most of them cold while explaining your thinking out loud, you are at the level.

Schema used throughout:
```
orders(order_id, customer_id, order_date, amount, status)
customers(customer_id, name, country, signup_date)
order_items(order_id, product_id, quantity, unit_price)
products(product_id, name, category)
employees(emp_id, name, manager_id, salary, dept_id)
logins(user_id, login_date)
orders_df, customers_df  -- pandas versions of orders and customers
```

---

## SQL (PostgreSQL) — 10

**S1. Second-highest order amount (distinct), handling ties.**
```sql
SELECT MAX(amount) AS second_highest
FROM orders
WHERE amount < (SELECT MAX(amount) FROM orders);
```
*Also know the DENSE_RANK version: rank amounts descending, filter `rnk = 2`.*

**S2. Customers who have ordered before, but not in the last 90 days.**
```sql
SELECT c.customer_id, c.name
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
HAVING MAX(o.order_date) < CURRENT_DATE - INTERVAL '90 days';
```

**S3. Delete duplicate orders (same customer, date, and amount), keeping the lowest `order_id`.**
```sql
DELETE FROM orders a
USING orders b
WHERE a.order_id > b.order_id
  AND a.customer_id = b.customer_id
  AND a.order_date  = b.order_date
  AND a.amount      = b.amount;
```

**S4. Employees who earn more than their manager.**
```sql
SELECT e.name
FROM employees e
JOIN employees m ON e.manager_id = m.emp_id
WHERE e.salary > m.salary;
```

**S5. Top 3 distinct salaries per department.**
```sql
WITH ranked AS (
    SELECT name, dept_id, salary,
           DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
    FROM employees
)
SELECT name, dept_id, salary
FROM ranked
WHERE rnk <= 3;
```

**S6. 7-day moving average of daily completed revenue.**
```sql
WITH daily AS (
    SELECT order_date::date AS d, SUM(amount) AS rev
    FROM orders
    WHERE status = 'completed'
    GROUP BY 1
)
SELECT d, rev,
       AVG(rev) OVER (ORDER BY d ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma7
FROM daily;
```
*Mention the catch: this is row-based, so missing dates shrink the window. Fix by joining to a generated date series first.*

**S7. Days between each customer's first and second order.**
```sql
WITH o AS (
    SELECT customer_id, order_date,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS rn
    FROM orders
)
SELECT a.customer_id, b.order_date - a.order_date AS days_between
FROM o a
JOIN o b ON a.customer_id = b.customer_id AND a.rn = 1 AND b.rn = 2;
```

**S8. Each category's share of total revenue, as a percentage.**
```sql
SELECT p.category,
       SUM(oi.quantity * oi.unit_price) AS revenue,
       ROUND(100.0 * SUM(oi.quantity * oi.unit_price)
             / SUM(SUM(oi.quantity * oi.unit_price)) OVER (), 2) AS pct_of_total
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
GROUP BY p.category;
```

**S9. Customers who ordered in every month of Q1 2026.**
```sql
SELECT customer_id
FROM orders
WHERE order_date >= '2026-01-01' AND order_date < '2026-04-01'
GROUP BY customer_id
HAVING COUNT(DISTINCT DATE_TRUNC('month', order_date)) = 3;
```

**S10. Users with a login streak of 3 or more consecutive days.**
```sql
WITH d AS (
    SELECT DISTINCT user_id, login_date FROM logins
),
g AS (
    SELECT user_id, login_date,
           login_date - (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date))::int AS grp
    FROM d
)
SELECT user_id, MIN(login_date) AS streak_start, MAX(login_date) AS streak_end, COUNT(*) AS days
FROM g
GROUP BY user_id, grp
HAVING COUNT(*) >= 3;
```

---

## Python — 10

**P1. Two-sum: return the indices of two numbers that add up to a target.**
```python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []
```

**P2. Group a list of words into anagram groups.**
```python
from collections import defaultdict

def group_anagrams(words):
    groups = defaultdict(list)
    for w in words:
        groups["".join(sorted(w))].append(w)
    return list(groups.values())
```

**P3. Check whether a string is a palindrome, ignoring case and non-alphanumeric characters.**
```python
def is_palindrome(s):
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]
```

**P4. Merge overlapping intervals (input as lists, e.g. `[[1,3],[2,6],[8,10]]`).**
```python
def merge_intervals(intervals):
    intervals = sorted(intervals, key=lambda x: x[0])
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
```

**P5. Return the k most frequent words.**
```python
from collections import Counter

def top_k(words, k):
    return [w for w, _ in Counter(words).most_common(k)]
```

**P6. Count log lines per level. Lines look like `"2026-01-01 12:00:00 ERROR payment failed"`.**
```python
from collections import Counter

def count_levels(lines):
    counts = Counter()
    for line in lines:
        parts = line.split(maxsplit=3)
        if len(parts) >= 3:
            counts[parts[2]] += 1
    return dict(counts)
```

**P7. Flatten a nested dict into dotted keys: `{"a": {"b": 1}}` becomes `{"a.b": 1}`.**
```python
def flatten(d, parent=""):
    out = {}
    for k, v in d.items():
        key = f"{parent}.{k}" if parent else k
        if isinstance(v, dict):
            out.update(flatten(v, key))
        else:
            out[key] = v
    return out
```

**P8. Sum a numeric column of a large CSV without loading it all into memory. Skip bad values and report how many were skipped.**
```python
import csv

def sum_column(path, col):
    total, skipped = 0.0, 0
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            try:
                total += float(row[col])
            except (ValueError, TypeError):
                skipped += 1
    return total, skipped
```

**P9. Return the index of the first non-repeating character in a string, or -1.**
```python
from collections import Counter

def first_unique(s):
    counts = Counter(s)
    for i, c in enumerate(s):
        if counts[c] == 1:
            return i
    return -1
```

**P10. Check whether a string of brackets `()[]{}` is balanced.**
```python
def is_balanced(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack
```

---

## Pandas — 10

**D1. Clean statuses, drop missing amounts, and keep completed orders over 100.**
```python
df = orders_df.copy()
df["status"] = df["status"].str.strip().str.lower()
result = df.dropna(subset=["amount"]).query("status == 'completed' and amount > 100")
```

**D2. Top 3 customers by total revenue, with their names.**
```python
top = (
    orders_df.groupby("customer_id", as_index=False)["amount"].sum()
    .nlargest(3, "amount")
    .merge(customers_df[["customer_id", "name"]], on="customer_id")
)
```

**D3. Month-over-month revenue growth (%).**
```python
orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
monthly = orders_df.groupby(orders_df["order_date"].dt.to_period("M"))["amount"].sum()
growth = monthly.pct_change() * 100
```

**D4. Daily revenue with a 7-day rolling average.**
```python
daily = orders_df.set_index("order_date")["amount"].resample("D").sum()
ma7 = daily.rolling(7).mean()
```

**D5. Customers who have never placed an order.**
```python
no_orders = customers_df[~customers_df["customer_id"].isin(orders_df["customer_id"])]
```

**D6. Keep only the latest row per `order_id`.**
```python
latest = orders_df.sort_values("order_date").drop_duplicates("order_id", keep="last")
```

**D7. Revenue pivot: countries as rows, months as columns.**
```python
merged = orders_df.merge(customers_df, on="customer_id")
merged["month"] = merged["order_date"].dt.to_period("M")
pivot = merged.pivot_table(
    index="country", columns="month", values="amount", aggfunc="sum", fill_value=0
)
```

**D8. Per-customer stats: first order, last order, order count, total spend.**
```python
stats = orders_df.groupby("customer_id").agg(
    first_order=("order_date", "min"),
    last_order=("order_date", "max"),
    orders=("order_id", "count"),
    total=("amount", "sum"),
).reset_index()
```

**D9. The top-spending customer in each country.**
```python
spend = merged.groupby(["country", "customer_id"], as_index=False)["amount"].sum()
top_per_country = spend.loc[spend.groupby("country")["amount"].idxmax()]
```

**D10. Flag outlier orders: more than 3 standard deviations from that customer's mean.**
```python
g = orders_df.groupby("customer_id")["amount"]
orders_df["z"] = (orders_df["amount"] - g.transform("mean")) / g.transform("std")
outliers = orders_df[orders_df["z"].abs() > 3]
```

---

## Requests — 3

**R1. Fetch JSON with a timeout. On failure, log the error and return `None`.**
```python
import logging
import requests

logger = logging.getLogger(__name__)

def fetch_json(url, params=None):
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        logger.error("Request failed: %s", e)
        return None
```

**R2. Fetch many IDs in parallel. One failure must not stop the others.**
```python
from concurrent.futures import ThreadPoolExecutor
import requests

def fetch_one(item_id):
    try:
        r = requests.get(f"{BASE_URL}/{item_id}", timeout=5)
        r.raise_for_status()
        return item_id, r.json(), None
    except requests.RequestException as e:
        return item_id, None, str(e)

with ThreadPoolExecutor(max_workers=5) as ex:
    results = list(ex.map(fetch_one, ids))

good = [(i, data) for i, data, err in results if err is None]
bad = [(i, err) for i, data, err in results if err is not None]
```

**R3. Handle HTTP 429 (rate limiting) by waiting for the `Retry-After` header, up to 3 attempts.**
```python
import time
import requests

def get_with_rate_limit(url, params=None, max_retries=3):
    for _ in range(max_retries):
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 429:
            time.sleep(int(resp.headers.get("Retry-After", 1)))
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError("Rate limited too many times")
```

---

## Pydantic — 3

**Y1. Validate a batch of rows. Collect valid models and errors separately, with the row index.**
```python
from pydantic import BaseModel, Field, ValidationError, field_validator

class Order(BaseModel):
    id: int
    amount: float = Field(gt=0)
    status: str

    @field_validator("status")
    @classmethod
    def normalize(cls, v):
        return v.strip().lower()

def split_valid(rows):
    valid, errors = [], []
    for i, row in enumerate(rows):
        try:
            valid.append(Order.model_validate(row))
        except ValidationError as e:
            errors.append((i, e.errors()))
    return valid, errors
```

**Y2. Parse an API payload with camelCase keys (`orderId`, `createdAt`) into snake_case fields, with the date parsed.**
```python
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class ApiOrder(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    order_id: int = Field(alias="orderId")
    created_at: datetime = Field(alias="createdAt")

o = ApiOrder.model_validate({"orderId": "7", "createdAt": "2026-01-15T10:00:00"})
o.model_dump()   # {"order_id": 7, "created_at": datetime(...)}
```

**Y3. A customer model with an optional nested address and a tags list. Dump it to a dict without `None` values.**
```python
from pydantic import BaseModel, Field

class Address(BaseModel):
    city: str
    country: str

class Customer(BaseModel):
    id: int
    name: str
    address: Address | None = None
    tags: list[str] = Field(default_factory=list)

c = Customer(id=1, name="Alice")
c.model_dump(exclude_none=True)   # {"id": 1, "name": "Alice", "tags": []}
```

---

## pytest — 2

**T1. Test a cleaning function with several edge cases, plus an expected exception with a message.**
```python
import pytest

@pytest.mark.parametrize("raw, expected", [
    ("  Completed ", "completed"),
    ("PENDING", "pending"),
    ("", ""),
    (None, None),
])
def test_clean_status(raw, expected):
    assert clean_status(raw) == expected

def test_validate_amount_rejects_negative():
    with pytest.raises(ValueError, match="negative"):
        validate_amount(-5)
```

**T2. Test `fetch_json` from R1 without making real network calls: one success case, one failure case.**
```python
from unittest.mock import Mock, patch
import requests

def test_fetch_json_success():
    fake = Mock()
    fake.json.return_value = {"id": 1}
    fake.raise_for_status.return_value = None
    with patch("mymodule.requests.get", return_value=fake) as mock_get:
        assert fetch_json("http://x", params={"page": 1}) == {"id": 1}
        mock_get.assert_called_once_with("http://x", params={"page": 1}, timeout=10)

def test_fetch_json_returns_none_on_error():
    with patch("mymodule.requests.get", side_effect=requests.ConnectionError("boom")):
        assert fetch_json("http://x") is None
```

---

## SQLAlchemy — 2

**A1. Using the ORM (2.0 style), total spend per customer, only customers over 100, highest first.**
```python
from sqlalchemy import select, func
from sqlalchemy.orm import Session

stmt = (
    select(Customer.name, func.sum(Order.amount).label("total"))
    .join(Order, Order.customer_id == Customer.id)
    .group_by(Customer.name)
    .having(func.sum(Order.amount) > 100)
    .order_by(func.sum(Order.amount).desc())
)

with Session(engine) as session:
    rows = session.execute(stmt).all()
```

**A2. Bulk upsert into Postgres: insert new orders, and update `amount` if the `order_id` already exists.**
```python
from sqlalchemy.dialects.postgresql import insert

stmt = insert(Order).values(rows)   # rows = list of dicts
stmt = stmt.on_conflict_do_update(
    index_elements=["order_id"],
    set_={"amount": stmt.excluded.amount},
)

with Session(engine) as session:
    session.execute(stmt)
    session.commit()
```
*Idempotent loads like this come up constantly in data-engineering interviews.*

---

## How to Use This

Don't read it front to back. Pick 5 questions, cover the code, and write your answer cold. Say your approach out loud as you write. Check yourself afterward, then repeat the same 5 tomorrow. If most of these come out cold in 10-20 minutes each, you're at the level.

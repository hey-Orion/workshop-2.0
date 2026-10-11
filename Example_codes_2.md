Interview Level

These are NOT warm-ups. Each one combines 2+ patterns, uses messier/more realistic data, or stacks multiple steps into one task — this is closer to what you'll actually hit live. If the earlier file was the vocabulary, this is a sentence.

Shared schema (extended from before):
```
orders(order_id, customer_id, order_date, amount, status)
customers(customer_id, name, country, signup_date)
order_items(order_id, product_id, quantity, unit_price)
products(product_id, name, category, price)
```

---

## 1. SQL (PostgreSQL) — Hard Tier

**Q1 — Window frame + running average + multi-condition filter**
*"For each customer's most recent completed order, show how it compares to their running average spend up to that point — but only for customers with 3+ completed orders."*
```sql
WITH customer_orders AS (
    SELECT customer_id, order_id, order_date, amount,
        AVG(amount) OVER (
            PARTITION BY customer_id ORDER BY order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
        ) AS running_avg,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn,
        COUNT(*) OVER (PARTITION BY customer_id) AS order_count
    FROM orders
    WHERE status = 'completed'
)
SELECT customer_id, order_id, amount, running_avg,
    CASE WHEN amount > running_avg THEN 'above' ELSE 'below' END AS vs_avg
FROM customer_orders
WHERE rn = 1 AND order_count >= 3;
```
*Why it's hard: the window frame (`ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING`) excludes the current row from its own average — easy to get backwards. Three separate conditions (most-recent, min-order-count, above/below) all have to land in one query.*

**Q2 — Self-join for period-over-period comparison**
*"Month-over-month spend change per customer, including customers with no orders in the prior month."*
```sql
WITH monthly AS (
    SELECT customer_id, DATE_TRUNC('month', order_date) AS month, SUM(amount) AS total
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id, DATE_TRUNC('month', order_date)
)
SELECT curr.customer_id, curr.month, curr.total AS this_month,
    prev.total AS last_month,
    ROUND(((curr.total - prev.total) / NULLIF(prev.total, 0)) * 100, 1) AS pct_change
FROM monthly curr
LEFT JOIN monthly prev
    ON curr.customer_id = prev.customer_id
    AND prev.month = curr.month - INTERVAL '1 month';
```
*Why it's hard: self-join on a derived table with a shifted date key, plus `NULLIF` to avoid a division-by-zero crash — a real bug if forgotten.*

**Q3 — Multi-table join + conditional aggregation**
*"Revenue by product category, completed orders only, from customers who signed up in the last 12 months."*
```sql
SELECT p.category, SUM(oi.quantity * p.price) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
    AND c.signup_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY p.category
ORDER BY revenue DESC;
```
*Why it's hard: four tables, and the filter conditions sit on two different tables (`orders.status`, `customers.signup_date`) while the aggregation key comes from a third (`products.category`) — easy to filter on the wrong table or at the wrong join stage.*

**Q4 — Percentile ranking**
*"Customers in the top 20% by total completed spend."*
```sql
WITH spend AS (
    SELECT customer_id, SUM(amount) AS total_spend
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
),
ranked AS (
    SELECT customer_id, total_spend,
        PERCENT_RANK() OVER (ORDER BY total_spend DESC) AS pct_rank
    FROM spend
)
SELECT customer_id, total_spend
FROM ranked
WHERE pct_rank <= 0.2;
```
*Why it's hard: `PERCENT_RANK()` can't be filtered in the same query level it's defined in (no `QUALIFY` in Postgres) — you need the extra CTE layer just to filter on it. A common trap.*

**Q5 — Gaps-and-islands (consecutive-months streak)**
*"Customers who placed at least one completed order in 3 or more consecutive months."*
```sql
WITH monthly AS (
    SELECT DISTINCT customer_id, DATE_TRUNC('month', order_date) AS month
    FROM orders WHERE status = 'completed'
),
numbered AS (
    SELECT customer_id, month,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY month) AS rn
    FROM monthly
),
grouped AS (
    SELECT customer_id, month,
        month - (rn || ' months')::interval AS grp
    FROM numbered
)
SELECT customer_id, COUNT(*) AS streak_length, MIN(month) AS streak_start
FROM grouped
GROUP BY customer_id, grp
HAVING COUNT(*) >= 3;
```
*Why it's hard: this is the "gaps and islands" pattern — subtracting a row number from a date to create a constant "group key" for consecutive values. Not something you'll derive from first principles under pressure; worth recognizing by name and knowing the trick (subtract `rn` months from `month`) cold.*

---

## 2. Python (Core) — Hard Tier

**Q1 — Multi-field validation with error collection, not just rejection**
*"Process a list of transaction dicts. Sum amounts per currency, but skip and log any record with a missing field, non-numeric amount, or negative amount — don't just crash or silently drop."*
```python
def process_transactions(transactions):
    summary = {}
    errors = []
    for i, tx in enumerate(transactions):
        try:
            currency = tx["currency"]
            amount = float(tx["amount"])
            if amount < 0:
                raise ValueError("negative amount")
        except (KeyError, ValueError, TypeError) as e:
            errors.append((i, str(e)))
            continue
        summary[currency] = summary.get(currency, 0) + amount
    return summary, errors
```

**Q2 — Merge with conflict resolution**
*"Merge two dicts of customer records keyed by id. On conflict, keep whichever record has the newer `updated_at`."*
```python
def merge_records(primary, secondary):
    merged = dict(secondary)
    for key, record in primary.items():
        if key not in merged or record["updated_at"] > merged[key]["updated_at"]:
            merged[key] = record
    return merged
```

**Q3 — Generator-based batching**
*"Write a generator that yields fixed-size batches from any iterable — used for chunking API calls or bulk inserts."*
```python
def batch(iterable, size):
    current = []
    for item in iterable:
        current.append(item)
        if len(current) == size:
            yield current
            current = []
    if current:
        yield current
```

**Q4 — Stateful decorator (TTL cache)**
*"Write a decorator that caches a function's result for N seconds, then re-computes."*
```python
import time
import functools

def ttl_cache(seconds):
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache and now - cache[args][1] < seconds:
                return cache[args][0]
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator
```
*Why it's hard: closures holding mutable state across calls, keying a cache by function arguments, and handling expiry — several moving parts in one small function.*

**Q5 — Multi-step pipeline (flatten → dedupe → sort)**
*"Given nested groups of records, flatten them, drop duplicates by id keeping the first occurrence, then sort by amount descending — one function."*
```python
def clean_pipeline(nested_records):
    seen = set()
    flat = []
    for group in nested_records:
        for record in group:
            if record["id"] not in seen:
                seen.add(record["id"])
                flat.append(record)
    return sorted(flat, key=lambda r: r["amount"], reverse=True)
```

---

## 3. Pandas — Hard Tier

**Q1 — Clean + dedupe + rolling average + flag, as one task**
*"Clean messy status strings, drop rows with missing amounts, keep only the latest row per duplicate order_id, then flag any order that deviates more than 50% from that customer's prior 3-order rolling average."*
```python
orders_df['status'] = orders_df['status'].str.strip().str.lower()
orders_df = orders_df.dropna(subset=['amount'])
orders_df = orders_df.sort_values('order_date').drop_duplicates(subset='order_id', keep='last')

orders_df['rolling_avg'] = (
    orders_df.sort_values('order_date')
    .groupby('customer_id')['amount']
    .transform(lambda s: s.shift().rolling(3, min_periods=1).mean())
)

orders_df['deviation_flag'] = (
    (orders_df['amount'] - orders_df['rolling_avg']).abs() / orders_df['rolling_avg'] > 0.5
)
```
*Why it's hard: `.shift()` before `.rolling()` is what keeps the current row out of its own average — a subtle, easy-to-miss detail, stacked on top of cleaning and dedup steps that have to happen in the right order.*

**Q2 — Merge that creates duplication, then aggregate it away**
*"Join orders with order_items (multiple rows per order), then roll back up to one revenue total per order."*
```python
merged = orders_df.merge(order_items_df, on='order_id', how='left')

revenue_by_order = (
    merged.assign(line_total=merged['quantity'] * merged['unit_price'])
    .groupby('order_id')['line_total']
    .sum()
    .reset_index(name='order_revenue')
)
```
*Why it's hard: the merge itself duplicates order-level columns across every item row — if you don't re-aggregate afterward, you'll double-count the order amount. This exact mistake is a very common real bug.*

**Q3 — groupby().apply() with custom multi-value logic**
*"For each customer, compute days between their first and most recent order, and their order frequency (orders per day)."*
```python
def customer_tenure(group):
    span_days = (group['order_date'].max() - group['order_date'].min()).days
    freq = len(group) / span_days if span_days > 0 else None
    return pd.Series({'tenure_days': span_days, 'order_frequency': freq})

tenure_df = orders_df.groupby('customer_id').apply(customer_tenure).reset_index()
```
*Why it's hard: `.agg()` can't return two unrelated derived values from the same group — this needs `.apply()` with a function returning a `Series`, plus a guard against division by zero for single-order customers.*

**Q4 — Pivot then reshape back (round trip)**
*"Total spend per customer per status, pivoted wide, then melted back to long form for a downstream chart."*
```python
pivoted = orders_df.pivot_table(
    index='customer_id', columns='status', values='amount',
    aggfunc='sum', fill_value=0
)

melted = pivoted.reset_index().melt(
    id_vars='customer_id', var_name='status', value_name='total_amount'
)
```

**Q5 — Date-indexed resampling**
*"Daily revenue, then a 7-day rolling average on top of it."*
```python
daily = orders_df.set_index('order_date').resample('D')['amount'].sum()
rolling_7d = daily.rolling('7D').mean()
```
*Why it's hard: requires a datetime index before `.resample()` works at all — forgetting `.set_index()` first is the most common way this breaks.*

---

## 4. Requests — Hard Tier

**Q1 — Paginated API fetch**
*"Fetch every page of results from a paginated API until there's no 'next' link."*
```python
def fetch_all_pages(base_url, params=None):
    results = []
    url = base_url
    while url:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results.extend(data["results"])
        url = data.get("next")
        params = None
    return results
```

**Q2 — Session reuse with automatic retry/backoff**
*"Make repeated calls to a flaky endpoint resilient to transient 5xx errors."*
```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

response = session.get(url, timeout=10)
```

**Q3 — Per-item failure isolation in a batch**
*"Fetch records for a list of IDs; one bad ID shouldn't kill the whole batch."*
```python
def fetch_many(ids, base_url):
    results, failures = [], []
    for item_id in ids:
        try:
            resp = requests.get(f"{base_url}/{item_id}", timeout=5)
            resp.raise_for_status()
            results.append(resp.json())
        except requests.RequestException as e:
            failures.append((item_id, str(e)))
    return results, failures
```

**Q4 — Token refresh on 401**
*"A client whose token expires mid-session should refresh once and retry, not just fail."*
```python
class APIClient:
    def __init__(self, token, base_url):
        self.token = token
        self.base_url = base_url

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def get(self, path):
        resp = requests.get(f"{self.base_url}{path}", headers=self._headers(), timeout=5)
        if resp.status_code == 401:
            self.token = self._refresh_token()
            resp = requests.get(f"{self.base_url}{path}", headers=self._headers(), timeout=5)
        resp.raise_for_status()
        return resp.json()

    def _refresh_token(self):
        resp = requests.post(f"{self.base_url}/refresh", timeout=5)
        resp.raise_for_status()
        return resp.json()["access_token"]
```

---

## 5. SQLAlchemy — Hard Tier

**Q1 — Relationship + eager loading**
*"Model a one-to-many customer→orders relationship and fetch customers with their orders in one query, not N+1."*
```python
class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    orders = relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    amount = Column(Float)
    customer = relationship("Customer", back_populates="orders")

customers = session.query(Customer).options(joinedload(Customer.orders)).all()
```

**Q2 — Bulk insert**
*"Insert 10,000 rows efficiently — not one `session.add()` + `commit()` per row."*
```python
session.bulk_insert_mappings(Order, [
    {"customer_id": 1, "amount": 50.0},
    {"customer_id": 2, "amount": 75.0},
])
session.commit()
```

**Q3 — Transaction with rollback on failure**
```python
try:
    order = Order(customer_id=1, amount=100.0)
    session.add(order)
    session.commit()
except Exception:
    session.rollback()
    raise
finally:
    session.close()
```

**Q4 — Aggregation through the ORM**
*"Total spend per customer, only customers over €100, using the ORM not raw SQL."*
```python
from sqlalchemy import func

results = (
    session.query(Order.customer_id, func.sum(Order.amount).label("total"))
    .group_by(Order.customer_id)
    .having(func.sum(Order.amount) > 100)
    .all()
)
```

---

## 6. pytest — Hard Tier

**Q1 — Fixture with setup/teardown**
```python
@pytest.fixture
def db_session():
    session = create_test_session()
    yield session
    session.rollback()
    session.close()

def test_insert_order(db_session):
    order = Order(customer_id=1, amount=50)
    db_session.add(order)
    db_session.commit()
    assert db_session.query(Order).count() == 1
```

**Q2 — Parametrized test**
```python
@pytest.mark.parametrize("amount,expected", [
    (600, "high"), (200, "medium"), (5, "low"),
])
def test_value_flag(amount, expected):
    assert flag_value(amount) == expected
```

**Q3 — Mocking an external call**
```python
def test_fetch_data(monkeypatch):
    class MockResponse:
        def json(self):
            return {"id": 1}
        def raise_for_status(self):
            pass

    monkeypatch.setattr(requests, "get", lambda *a, **kw: MockResponse())
    result = fetch_data("http://fake-url")
    assert result["id"] == 1
```

**Q4 — Parametrized exception testing**
```python
@pytest.mark.parametrize("payload", [
    {"id": "bad"},
    {},
])
def test_invalid_payloads(payload):
    with pytest.raises(ValidationError):
        OrderSchema.model_validate(payload)
```

---

## 7. Pydantic — Hard Tier

**Q1 — Nested models**
```python
class Address(BaseModel):
    city: str
    country: str

class Customer(BaseModel):
    id: int
    name: str
    address: Address

c = Customer.model_validate({
    "id": 1, "name": "Alice",
    "address": {"city": "Berlin", "country": "DE"},
})
```

**Q2 — Custom field validator**
```python
from pydantic import field_validator

class OrderSchema(BaseModel):
    id: int
    amount: float
    status: str

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("amount must be positive")
        return v
```

**Q3 — Default factory for mutable/dynamic defaults**
```python
from pydantic import Field
from datetime import datetime

class Order(BaseModel):
    id: int
    amount: float
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Q4 — Cross-field validation**
```python
from pydantic import model_validator

class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime

    @model_validator(mode="after")
    def check_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be after start_date")
        return self
```

---

## How to Use This

Same drilling method, raised a notch: read once, close it, attempt cold. If you can only solve these with the file open, that's the real signal — it means the earlier "basic" set built the vocabulary but you haven't yet practiced combining it under pressure, which is exactly what real interviews test.

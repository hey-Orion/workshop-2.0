WITH customer_totals AS (
    SELECT
        c.customer_id,
        c.name,
        SUM(o.amount) AS total_spend
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
),
ranked AS (
    SELECT
        customer_id,
        name,
        total_spend,
        PERCENT_RANK() OVER (ORDER BY total_spend DESC) AS pct_rank
    FROM customer_totals
)
SELECT customer_id, name, total_spend
FROM ranked
WHERE pct_rank <= 0.10;

import pandas as pd

# Drop exact duplicate rows
orders_df = orders_df.drop_duplicates()

# Drop rows with missing amount (can't sum an unknown value)
orders_df = orders_df.dropna(subset=['amount'])

orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
orders_df['month'] = orders_df['order_date'].dt.to_period('M')

monthly_revenue = (
    orders_df.groupby(['customer_id', 'month'])['amount']
    .sum()
    .reset_index()
)

def get_average(amounts):
    if not amounts:
        return 0
    total = 0
    for amt in amounts:
        total += amt
    return total / len(amounts)
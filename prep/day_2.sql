orders(order_id, customer_id, order_date, amount, status)
customers(customer_id, name, country, signup_date)

-- Sequential Order Amount Comparison (LAG)
SELECT
    order_id,
    customer_id,
    order_date,
    amount,
    LAG(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date ASC, order_id ASC
    ) AS previous_order_amount
FROM orders;


-- Customer Revenue Ranking
WITH customer_aggregates AS (
    SELECT  
        c.customer_id,
        c.name,
        SUM(o.amount) AS total_spend
    FROM customers c 
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
)
SELECT
    name,
    total_spend,
    DENSE_RANK() OVER (
        ORDER BY total_spend DESC, customer_id ASC 
    ) AS customer_rank
FROM customer_aggregates;


-- Deviation from Customer Average Spend
SELECT
    order_id,
    customer_id,
    amount,
    AVG(amount) OVER (
        PARTITION BY customer_id
    ) AS customer_avg_amount,
    amount - AVG(amount) OVER (
        PARTITION BY customer_id
    ) AS amount_diff
FROM orders;


-- Section B: CTE-Driven Aggregations & Analytical Filtering

-- Above-Average Revenue Customers via CTE
WITH customer_totals AS (
    SELECT  
        c.customer_id,
        c.name,
        SUM(o.amount) AS total_amount
    FROM customers c 
    JOIN orders o ON c.customer_id = o.customer_id 
    GROUP BY c.customer_id, c.name 
),
global_avg_customer_spend AS (
    SELECT 
        AVG(total_amount) AS avg_customer_spend
    FROM customer_totals
)
SELECT
    ct.customer_id,
    ct.name,
    ct.total_amount
FROM customer_totals ct
CROSS JOIN global_avg_customer_spend g
WHERE ct.total_amount > g.avg_customer_spend;


-- Second-Highest Order Amount per Customer
WITH ranked_orders AS (
    SELECT
        customer_id,
        order_id,
        order_date,
        amount,
        DENSE_RANK() OVER (
            PARTITION BY customer_id
            ORDER BY amount DESC, order_id ASC 
        ) AS rnk 
    FROM orders 
)
SELECT
    customer_id,
    order_id,
    order_date,
    amount
FROM ranked_orders
WHERE rnk = 2;
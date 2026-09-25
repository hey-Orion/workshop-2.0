-- Q1: Basic JOIN + WHERE
SELECT 
    c.customer_id,
    c.name, 
    o.amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id 
WHERE c.country = 'Germany' 
  AND o.amount > 100 
ORDER BY c.customer_id;

-- Q2: GROUP BY + Aggregate + HAVING
SELECT 
    c.country, 
    SUM(o.amount) AS total_amount,
    COUNT(o.order_id) AS total_orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.country
HAVING COUNT(o.order_id) > 5;

-- Q3: Running Total Window Function
SELECT 
    order_id,
    customer_id,
    order_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date
    ) AS running_total
FROM orders;

-- Q4: CTE + Aggregates
WITH customers_total AS (
    SELECT
        customer_id, 
        SUM(amount) AS total_amount
    FROM orders 
    GROUP BY customer_id
)
SELECT customer_id, total_amount 
FROM customers_total
ORDER BY total_amount DESC
LIMIT 3;

-- Q5: CTE + Ranking Window Function
WITH customers_orders AS (
    SELECT
        customer_id,
        amount,
        order_date,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY amount DESC
        ) AS rn 
    FROM orders 
)
SELECT 
    customer_id, 
    amount,
    order_date
FROM customers_orders
WHERE rn = 1;
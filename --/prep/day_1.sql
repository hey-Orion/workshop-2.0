orders(order_id, customer_id, order_date, amount, status)
customers(customer_id, name, country, signup_date)

-- Query 1: Filtered Customer Orders
SELECT 
    c.name,
    o.amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.country = 'Germany'
  AND o.amount > 100.00;

-- Query 2: Country Revenue Thresholds
SELECT 
    c.country,
    SUM(o.amount) AS total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.country
HAVING COUNT(o.order_id) > 5;

-- Query 3: Customer Cumulative Spend Trajectory
SELECT 
    order_id,
    customer_id,
    order_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id 
        ORDER BY order_date ASC, order_id ASC
    ) AS running_total
FROM orders;

-- Query 4: Top 3 High-Value Customers via CTE
WITH customer_spend AS (
    SELECT 
        c.customer_id,
        c.name,
        SUM(o.amount) AS total_spend
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
)
SELECT 
    customer_id,
    name,
    total_spend
FROM customer_spend
ORDER BY total_spend DESC
LIMIT 3;

-- Query 5: Highest Single-Value Order per Customer
WITH ranked_orders AS (
    SELECT 
        customer_id,
        order_id,
        order_date,
        amount,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id 
            ORDER BY amount DESC, order_id ASC
        ) AS rn
    FROM orders
)
SELECT 
    customer_id,
    order_id,
    order_date,
    amount
FROM ranked_orders
WHERE rn = 1;


-- Query 6: Completed Orders in France
SELECT 
    c.name, 
    o.amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.country = 'France'
  AND o.status = 'completed';

-- Query 7: Customers with More Than 3 Orders
SELECT 
    c.customer_id, 
    SUM(o.amount) AS total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
HAVING COUNT(o.order_id) > 3;

-- Query 8: Average Order Amount by Country
SELECT 
    c.country, 
    AVG(o.amount) AS avg_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.country
ORDER BY avg_amount DESC;

-- Query 9: Most Recent Order for Early Signups
SELECT 
    c.customer_id,
    c.name, 
    MAX(o.order_date) AS most_recent_order
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.signup_date < '2023-01-01'
GROUP BY c.customer_id, c.name;

-- Query 10: Customers with No Orders
SELECT 
    c.customer_id,
    c.name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

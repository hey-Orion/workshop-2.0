
select p.category, sum(o.total_amount) as revenue
from orders o 
join product p on o.product_id = p.product_id
where o.status = "completed"
group by p.category
order by revenue desc;

select customer_id, count(*) as order_count
from orders
where status = "completed"
group by customer_id
having count(*) > 5;

with ranked as (
    select
        ticket_id,
        status,
        updated_id,
        row_number() over (
            partition by ticket_id
            order by updated_id desc
        ) as rn 
    from ticket_update
)
select ticket_id, status, updated_id
from ranked 
where rn = 1;

# this needs to be explaned 
WITH signups AS (
    SELECT user_id, created_at FROM users
),
activated AS (
    SELECT DISTINCT user_id FROM events WHERE event_type = 'activated'
),
paid AS (
    SELECT DISTINCT user_id FROM subscriptions WHERE status = 'active'
)
SELECT
    COUNT(DISTINCT s.user_id) AS total_signups,
    COUNT(DISTINCT a.user_id) AS total_activated,
    COUNT(DISTINCT p.user_id) AS total_paid
FROM signups s
LEFT JOIN activated a ON s.user_id = a.user_id
LEFT JOIN paid p ON s.user_id = p.user_id;

SELECT e.name AS employee, m.name AS manager
FROM employees e
JOIN employees m ON e.manager_id = m.employee_id
WHERE e.salary > m.salary;

SELECT
    DATE_TRUNC('month', u.signup_date) AS cohort_month,
    COUNT(DISTINCT u.user_id) AS cohort_size,
    COUNT(DISTINCT CASE WHEN u.is_active THEN u.user_id END) AS still_active
FROM users u
GROUP BY DATE_TRUNC('month', u.signup_date)
ORDER BY cohort_month;
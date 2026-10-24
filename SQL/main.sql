orders(order_id, customer_id, order_date, amount, status)
customers(customer_id, name, country, signup_date)
order_items(order_id, product_id, quantity, unit_price)
products(product_id, name, category)
employees(emp_id, name, manager_id, salary, dept_id)
logins(user_id, login_date)

select
    c.name,
    coalesce(sum(case when o.status = 'completed' then o.amount else 0 end), 0) as total_completed_spend
from customers c 
left join orders o on c.customer_id = o.customer_id
group by c.customer_id, c.name;

select c.customer_id, c.name
from customers c 
left join orders o on c.customer_id = o.customer_id
where o.order_id is NULL;

with rankedorders as (
    select
        amount,
        dense_rank() over (partition by amount desc) as rnk 
    from orders
)
select distinct amount 
from rankedorders
where rnk = 2;

select
    e.emp_id,
    e.name as employee_name,
    e.salary as employee_salary,
    m.name as manager_name,
    m.salary as manager_salary
from employees e 
join employees m on e.manager_id = m.emp_id
where e.salary > m.salary;

select c.customer_id, c.name
from customers c 
where c.customer_id in (
    select customer_id
    from orders
    where order_date >= '2026-01-01' AND order_date < '2026-02-01'

    intersect

    select customer_id
    from orders
    WHERE order_date >= '2026-02-01' AND order_date < '2026-03-01'
);

select
    c.country
    count(o.order_id) as completed_orders_count
from customers c 
join orders o on c.customer_id = o.customer_id
where o.status = 'completed'
group by c.country
having count(o.order_id) > 5;

with categorized_orders as (
    select
        order_id,
        case
            when amount > 100 then 'high'
            when amount > 50 then 'mid'
            else 'low'
        end as order_label
    from orders 
)
select order_label, count(*) as order_count 
from categorized_orders
group by order_label;

select 
    p.category,
    SUM(oi.quantity * oi.unit_price) AS category_revenue,
    SUM(oi.quantity * oi.unit_price) * 100.0 / SUM(SUM(oi.quantity * oi.unit_price)) OVER() AS percentage_of_total
from order_items oi 
join products p on oi.product_id = p.product_id
group by p.category;

SELECT 
    customer_id,
    SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) AS completed_total,
    SUM(CASE WHEN status = 'pending' THEN amount ELSE 0 END) AS pending_total,
    SUM(CASE WHEN status = 'cancelled' THEN amount ELSE 0 END) AS cancelled_total
FROM orders
GROUP BY customer_id;

select order_id
from orders 
group by order_id
having count(*) > 1;

delete from orders 
where ctid not in (
    select min(ctid)
    from orders 
    group by order_id
);

with ranked_orders as (
    select *,
            row_number() over (partition by customer_id order by order_date desc) as rn
    from orders 
)
select *
from ranked_orders
where rn = 1;

with ranked_sal as (
    select *,
            dense_rank() over (partition by dept_id order by salary desc) as rnk
    from employees
)
select * 
from ranked_sal
where rnk <= 3;

select
    order_id,
    customer_id,
    order_date,
    amount,
    sum(amount) over (partition by customer_id order by order_date,order_id) as running_total
from orders;

select
    order_id,
    customer_id,
    order_date,
    amount,
    lag(amount) over (partition by customer_id order by order_date, order_id) as prev_amount
from orders;

with daily_rev as (
    select
        cast(order_date as date) as rev_date,
        sum(amount) as daily_rev
    from orders 
    where status = 'completed'
    group by cast(order_date as data)
)
select
    rev_date,
    daily_rev,
    avg(daily_rev) over (
        order by rev_date
        row between 6 preceding and current row 
    ) as moving_avg_7d
from daily_rev;

WITH ordered_customers AS (
    SELECT 
        customer_id,
        order_date,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS rn
    FROM orders
)
SELECT 
    c1.customer_id,
    c1.order_date AS first_order_date,
    c2.order_date AS second_order_date,
    DATEDIFF(day, c1.order_date, c2.order_date) AS days_between
FROM ordered_customers c1
JOIN ordered_customers c2 
  ON c1.customer_id = c2.customer_id 
 AND c1.rn = 1 
 AND c2.rn = 2;

with customer_spends as (
    select
        customer_id,
        sum(amount) as total_spend 
    from orders 
    group by customer_id
)
select customer_id, total_spend
from customer_spends
where total_spend > (select avg(total_spend) from customer_spends);

select customer_id
from orders 
where order_date >= '' and order_date < ''
group by customer_id
having count(distinct extract(month from order_date)) = 3;

WITH consecutive_logins AS (
    SELECT 
        user_id,
        login_date,
        DATE_SUB(login_date, INTERVAL ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) DAY) AS grp
    FROM logins
)
SELECT DISTINCT user_id
FROM consecutive_logins
GROUP BY user_id, grp
HAVING COUNT(*) >= 3;

WITH customer_signup_months AS (
    SELECT 
        customer_id,
        DATE_FORMAT(signup_date, '%Y-%m-01') AS signup_month
    FROM customers
)
SELECT 
    c.signup_month,
    COUNT(DISTINCT c.customer_id) AS total_signed_up,
    COUNT(DISTINCT o.customer_id) AS retained_customers,
    (COUNT(DISTINCT o.customer_id) * 100.0 / COUNT(DISTINCT c.customer_id)) AS retention_percentage
FROM customer_signup_months c
LEFT JOIN orders o 
  ON c.customer_id = o.customer_id 
 AND DATE_FORMAT(o.order_date, '%Y-%m') = DATE_FORMAT(DATE_ADD(CAST(c.signup_month AS DATE), INTERVAL 1 MONTH), '%Y-%m')
GROUP BY c.signup_month;
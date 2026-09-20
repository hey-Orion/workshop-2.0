# day_1, day_2

orders(order_id, customer_id, order_date, amount, status)
customers(customer_id, name, country, signup_date)

SELECT c.name, o.amount 
from customers c 
join orders o on c.customer_id = o.customer_id
where c.country = 'Germany'
and o.amount > 100.00;

SELECT
    c.country,
    sum(o.amount) as total_amount,
from customers c 
join orders o on c.customer_id = o.customer_id
group by c.country
having count(o.order_id) > 5;

SELECT
    order_id,
    customer_id,
    order_date,
    amount,
    sum(amount) over (
        PARTITION by customer_id
        order by order_date asc, order_id asc
    ) as running_total
from orders;

with customer_spend as (
    SELECT
        c.customer_id,
        o.name,
        sum(o.amount) as total_spend
    from customers c 
    join orders o on c.customer_id = o.customer_id
    group by c.customer_id, o.name
)
SELECT
    customer_id
    name
    total_spend
from customer_spend
order by total_spend DESC
limit 3;

with ranked_orders as (
    SELECT
       customer_id, 
       order_id, 
       order_date,
       amount,
       ROW_NUMBER() over (
        PARTITION by customer_id
        order by amount desc, order_id asc
       ) as rn 
    from orders
)
SELECT
    customer_id, 
    order_id, 
    order_date,
    amount
from ranked_orders
where rn = 1;


SELECT c.name, o.amount
from customers c 
join orders o on c.customer_id = o.customer_id
where c.country = 'French'
and o.status = 'completed';

SELECT c.customer_id, sum(o.amount) as total_amount
from customers c 
join orders o on c.customer_id = o.customer_id
having count(o.order_id) > 3;

SELECT 
    c.country
    avg(o.amount) as avg_amount
from customers c 
join orders o on c.customer_id = o.customer_id
group by c.country
order by avg_amount desc;


SELECT
    c.customer_id,
    c.name,
    max(o.order_date) as most_recent_order
from customers
join orders o on c.customer_id = o.customer_id
where c.signup_date < '2023-01-01'
group by c.customer_id, c.name;

SELECT 
    c.customer_id,
    c.name
from customers c 
left join orders o on c.customer_id = o.customer_id
where o.order_id is NULL;



SELECT 
    order_id,
    customer_id,
    order_date,
    amount,
    lag(amount) over (
        PARTITION by customer_id
        order by order_date asc, order_id asc 
    ) as previous_order_amount
from orders;

with customer_aggregates as (
    SELECT
        c.customer_id,
        c.name,
        sum(o.amount) as total_amount
    from customers c 
    join orders o on c.customer_id = o.customer_id
    group by c.customer_id, c.name
)
SELECT
    name,
    total_amount
    DENSE_RANK() over (
        order by total_spend desc, customer_id asc
    ) as customer_aggregates;

SELECT
    order_id,
    customer_id,
    amount,
    avg(amount) over (
        PARTITION by customer_id
    ) as amount_diff
from orders;

with customer_totals as (
    SELECT
        c.customer_id,
        c.name,
        sum(o.amount) as total_amount
    from customers c 
    join order o on c.customer_id = o.customer_id
    group by c.customer_id, c.name
)
global_avg_customer_spend as (
    SELECT 
        avg(total_amount) as avg_customer_spend
    from customer_totals
)
SELECT
    ct.customer_id,
    ct.name,
    ct.total_amount,
from customer_totals ct 
cross join global_avg_customer_spend g 
where ct.total_amount > g.avg_customer_spend;

with ranked_orders as (
    SELECT
        customer_id,
        order_id,
        order_date,
        amount,
        DENSE_RANK() over (
            PARTITION by customer_id
            order by amount desc, order_id ASC
        ) as rnk 
    from orders
)
SELECT
    customer_id,
    order_id,
    order_date,
    amount
from ranked_orders
where rnk = 2;

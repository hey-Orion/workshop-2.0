# day_1, day_2

orders(order_id, customer_id, order_date, amount, status)
customers(customer_id, name, country, signup_date)

select c.name, o.amount
from customers c 
join orders o on c.customer_id = o.customer_id
where c.country = 'Germany'
and o.amount > 100.00;

select c.country, sum(o.amount) as total_amount
from customers c 
join orders o on c.customer_id = o.customer_id
group by c.customer_id
having count(o.order_id) > 5;

select 
    order_id,
    customer_id,
    order_date,
    amount,
    sum(amount) over (
        partition by customer_id 
        order by order_date asc
    ) as running_total
from orders;

with customer_spend as (
    select
        c.customer_id,
        c.name
        sum(o.amount) as total_spend
    from customers c 
    join orders o on c.customer_id = o.customer_id
    group by c.customer_id, c.name
)
select customer_id, name, total_spend
from customer_spend
order by total_spend desc 
limit 3;

with ranked_orders as (
    select
        customer_id,
        order_id,
        order_date,
        amount,
        row_number() over (
            partition by customer_id order by amount desc, order_id asc
        ) as rn 
    from orders 
)
select customer_id, order_id, order_date, amount 
from ranked_orders
where rn = 1;


select c.name, o.amount
from customers c 
join orders o on c.customer_id = o.customer_id
where c.country = 'France'
and o.status = 'completed';

select c.customer_id, sum(o.amount) as total_amount
from customers c 
join orders o on c.customer_id = o.customer_id
group by c.customer_id
having count(order_id) > 3;

select c.country, avg(o.amount) as avg_amount
from customers c 
join orders o on c.customer_id = o.customer_id
group by c.country
order by avg_amount desc;

select c.name, max(o.order_date) as most_recent_order
from customers c 
join orders o on c.customer_id = o.customer_id
where c.signup_date < '2023-01-01'
group by c.name;

select c.name
from customers c 
left join orders o on c.customer_id = o.customer_id
where o.order_id is NULL;



select
    order_id,
    customer_id,
    order_date,
    amount,
    lag(amount) over (
        partition by customer_id 
        order by order_date asc, order_id asc
    ) as previous_order_amount
from orders;

with customer_aggregates as (
    select  
        c.customer_id,
        c.name,
        sum(o.amount) as total_spend
    from customers c 
    join orders o on c.customer_id = o.customer_id
    group by c.customer_id, c.name
)
select
    name,
    total_spend,
    dense_rank() over (
        order by total_spend desc, customer_id asc 
    ) as customer_rank
from customer_aggregates;

select
    order_id,
    customer_id,
    amount,
    avg(amount) over (
        partition by customer_id
    ) as customer_avg_amount,
    amount - avg(amount) over (
        partition by customer_id
    ) as amount_diff
from orders;

with customer_totals as (
    select  
        c.customer_id,
        c.name,
        sum(o.amount) as total_amount
    from customer c 
    join orders on c.customer_id = o.customer_id 
    group by c.customer_id, c.name 
),
global_avg_customer_spend as (
    select 
        avg(total_amount) as avg_customer_spend
    from customer_totals
)
SELECT #
    ct.customer_id,
    ct.name,
    ct.total_amount
FROM customer_totals ct
CROSS JOIN global_avg_customer_spend g
WHERE ct.total_amount > g.avg_customer_spend;

with ranked_orders as (
    select
        customer_id,
        order_id,
        order_date,
        amount,
        dense_rank() over (
            partition by customer_id
            order by amount desc, order_id asc 
        ) as rnk 
    from orders 
)
select
    customer_id,
    order_id,
    order_date,
    amount
from ranked_orders
where rnk = 2;

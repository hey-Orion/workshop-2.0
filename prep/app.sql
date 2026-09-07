select c.country, sum(o.amount) as total_revenue
from customers c 
join orders o on c.customer_id = o.customer_id
where o.status = 'completed'
  AND o.order_date >= '2025-01-01' AND o.order_date < '2026-01-01'
group by c.country
having sum(o.amount) > 10000;

select
    customer_id,
    order_date,
    amount,
    lag(amount) over (partition by customer_id order by order_date) as prev_amount
from orders;

with ranked as (
    select
        customer_id, order_id, amount,
        rank() over (partition by customer_id order by amount desc) as rnk 
    from orders
)
select customer_id, order_id, amount
from ranked
where rnk = 1;

select p.category, sum(oi.quantity) as total_units
from order_items oi 
join porduct p on oi.porduct_id = p.porduct_id
group by p.category
order by total_units desc;

select customer_id, order_date, count(*) as orders_that_day
from orders 
group by customer_id, order_date
having count(*) > 1;

select customer_id, avg(amount) as avg_amount
from orders 
where amount > (select avg(amount) from orders)
group by customer_id
order by avg_amount desc 
limit 5;

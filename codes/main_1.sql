select c.country, sum(o.amount) as total_rev
from customers c 
join orders o on c.customer_id = o.customer_id
where o.status == 'completed'
and o.amount > 100
group by c.country;

select c.country, count(o.order_id) as order_count
from customers c 
join orders on c.customer_id = o.customer_id
where o.status = 'completed'
group by c.country
having count(order_id) > 5;

select customer_id, order_date, amount,
    lag(amount) over (partition by customer_id order by order_date)
    as prev_amount
from orders;

with ranked as (
    select customer_id, order_id, amount,
        rank() over (partition by customer_id order by amount desc)
        as rnk 
    from orders 
)
select customer_id, order_id, amount 
from ranked 
where rnk = 1;

with totals as (
    select customer_id, sum(amount) as total_rev
    from orders
    group by customer_id
)
select customer_id, total_rev
from totals
where total_rev > (select avg(amount) from totals);
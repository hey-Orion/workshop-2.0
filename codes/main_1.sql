select c.country, sum(o.amount) as total_revenue
from customers c 
join orders o on c.customer_id = o.customer_id
where o.status = 'completed' and o.amount > 100
group by c.country;

select c.country, count(o.order_id) as order_count
from customers c 
join orders o on c.customer_id = o.customer_id
where o.status = 'completed'
group by c.country
having count(o.order_id) > 5;

select customer_id, order_date, amount,
    lag(amount) over (partition by customer_id order by order_date) as 
    prev_amount
from orders;

with ranked as (
    select customer_id, order_id, amount,
        rank() over (partition by customer_id order by amount desc) as rnk 
    from orders
)
select customer_id, order_id, amount from ranked where rnk = 1;

with totals as (
    select customer_id, sum(amount) as total_amount
    from orders group by customer_id
)
select customer_id, total_amount, from totals
where total_amount > (select avg(amount) from totals);
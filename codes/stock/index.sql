select customer_id, total_amount
from orders 
where total_amount > 100;

select customer_id, count(*) as total_orders
from orders 
group by customer_id
order by total_orders desc;

select c.region, avg(o.total_amount) as avg_order_amount
from orders o 
join customers c on c.customer_id = o.customer_id
group by c.region
order by c.region;

select *
from orders
where order_date >= current_date - interval '30 day';

select c.customer_id, c.name 
from customers c  
left join orders o on o.customer_id = c.customer_id
where o.order_id is null; 

with ranked_orders as (
    select
        customer_id,
        order_id,
        total_amount,
        row_number() over (partition by customer_id 
        order by total_amount desc) as rn
    from orders
)
select customer_id, order_id, total_amount
from ranked_orders
where rn = 1;


















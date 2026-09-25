select * from products
where price > 200;

select product_id, count(*) as total_orders
from orders 
order by product_id 
where total_orders desc;

select c.region, avg(o.total_amount) as avg_order
from orders o 
join customers c on c.customer_id = o.customer_id
group by c.region;

with ranked as (
    select *,
        row_number() over (partition by customer_id order by order_date desc) as rn
    from orders  
)
select * from ranked where rn = 1;

select c.customer_id, c.name
from customers c 
left join orders o on o.customer_id = c.customer_id
where o.customer_id is null;

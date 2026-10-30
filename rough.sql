select
    c.name,
    coalesce(sum(case when o.status = "completed" then o.amount else 0 end), 0) as TCS
from customers c 
left join orders o c.customer_id = o.customer_id
group by c.name, c.customer_id;

select c.customer_id, c.name 
from customers c 
join orders o on c.customer_id = o.customer_id
where o.order_id is null;

with RO as (
    select
        amount,
        dense_rank() over (order by amount desc) as rnk 
    from orders 
)
select distinct amount
from RO
where rnk = 2;

select
    status
    sum(amount) as total_rev,
    count(order_id) as total_orders
from orders 
group by status;

select
    name,
    signup_date
from customers 
where country = 'USA';

select
    c.name,
    sum(case when o.status = 'completed' then o.amount else 0 end) as total
from customers c 
left join orders o on c.customer_id = o.customer_id
group by c.customer_id, c.name;

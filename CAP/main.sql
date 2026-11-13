select * from orders 
where status = 'completed'
  and amount > 100
order by amount desc;

select
    c.name,
    sum(o.amount) as total_amount
from customers c 
join orders o on c.customer_id = o.customer_id
group by c.name, c.customer_id;

select
  c.name
from customers c 
where c.country = 'Germany'
order by c.name;

select
  status,
  count(order_id) as total_orders
from orders 
group by status;

select * from employees;

select * from products
where price > 50;

select
  count(order_id) as total_orders 
from orders;

select * from users 
order by created_id asc;

select distinct category
from products;
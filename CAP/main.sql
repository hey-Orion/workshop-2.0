orders(order_id, customer_id, order_date, amount, status)
customers(customer_id, name, country)

select * from orders 
where status = 'completed'
  and amount > 100
order by amount desc; i did group by insted of order by 

select
    c.name,
    sum(amount) as total_amount
from customers c 
join orders o on c.customer_id = o.customer_id
group by c.name, c.customer_id;


select customer_id, name need some fixing with this one but the strucher was right
from customers
where country = "Germany"
order by name;

select the error was a , and i dident add the status in the select
    status,
    count(order_id) as total_orders
from orders 
group by status;


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


select 
    name
from customers
where country = 'India'
order by name desc;

select *
from orders 
where status = 'refunded'
   and amount < 50;

select
    country,
    count(customer_id) as total_customers_per_country
from customers
group by country;

SELECT status, AVG(amount) AS avg_amount 
FROM orders 
GROUP BY status;

select
    c.customer_id
from customers c 
left join orders o on c.customer_id = o.customer_id
where o.order_id IS NULL;



orders(order_id, customer_id, order_date, amount, status)
customers(customer_id, name, country)

select * from customers
where country = 'India'
order by name desc;

select * from orders 
where status = 'refunded'
  and amount < 50;

select 
    country,
    count(customer_id) as total_customers_per_country
from customers
group by country;

select
    status,
    avg(amount) as avg_amount
from orders 
group by status

select c.customer_id
from customers c 
left join orders o on c.customer_id = o.customer_id 
where o.order_id is null;


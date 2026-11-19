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
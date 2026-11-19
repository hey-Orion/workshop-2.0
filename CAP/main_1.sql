select 
    name,
    customer_id
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

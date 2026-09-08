orders(order_id, customer_id, order_date, amount, status)
customers(customer_id, name, country, signup_date)

select c.name, o.amount
from customers c 
join orders o on c.customer_id = o.customer_id
where c.country = 'France'
and o.status = 'completed';

select c.customer_id, sum(o.amount) as total_amount
from customers c 
join orders o on c.customer_id = o.customer_id
group by c.customer_id
having count(o.order_id) > 3;

select c.country, avg(o.amount) as avg_amount
from customers c 
join orders o on c.customer_id = o.customer_id
group by c.country
order by avg_amount desc;

select c.name, max(o.order_date) as most_recent_order 
from customers c 
join orders o on c.customer_id = o.customer_id
where c.signup_date < '2023-01-01'
group by c.name;

select c.name
from customers c 
left join orders o on c.customer_id = o.customer_id
where o.order_id is null;

orders(order_id, customer_id, order_date, amount, status)
customers(customer_id, name, country)


select * these was some synex error with this but the strucher was right 
from orders 
where status = 'completed'
  and amount >= 100
order by amount desc;

select this alse had few synex error 
    c.name,
    sum(o.amount) as total_amount 
from orders o 
join customers c on c.customer_id = o.customer_id
group by c.customer_id, c.name;


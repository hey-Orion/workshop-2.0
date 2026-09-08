orders(order_id, customer_id, order_date, amount, status)
customers(customer_id, name, country, signup_date)


select 
    order_id, 
    customer_id, 
    order_date, 
    amount,
    lag(amount) over (partition by customer_id order by order_date) as previous_order_amount 
from orders;

select
    c.name,
    sum(o.amount) as total_amount,
    dense_rank() over (order by sum(o.amount) desc) as customer_rank
from customers c 
join orders o on c.customer_id = o.customer_id
group by c.name; 

select 
    order_id, 
    customer_id, 
    amount,
    amount - avg(amount) over (partition by customer_id) as deff_avg 
from orders ;

with customer_table as (
    select 
        customer_id,
        sum(amount) as total_amount 
    from orders 
    group by customer_id
)
select customer_id, total_amount
from customer_table
where total_amount > (select avg(total_amount) from customer_table);

with ranked_orders as (
    select
        customer_id,
        order_id,
        amount,
        dense_rank() over (partition by customer_id order by amount desc) as rnk
    from orders 
)
select customer_id, order_id, amount 
from ranked_orders
where rnk = 2;

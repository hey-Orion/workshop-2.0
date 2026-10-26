# solved
orders(order_id, customer_id, order_date, amount, status)
customers(customer_id, name, country, signup_date)
order_items(order_id, product_id, quantity, unit_price)
products(product_id, name, category)
employees(emp_id, name, manager_id, salary, dept_id)
logins(user_id, login_date)

Show each customer’s name and total completed spend, including customers with no orders (their total should show as 0).

select
    c.name,
    coalesce(sum(case when o.status = "completed" then o.amount else 0 end), 0) as TCS
from customers c 
left join orders o on c.customer_id = o.customer_id
group by c.customer_id, c.name;


Find customers who have never placed an order.

select c.customer_id, c.name
from customers c 
join orders o on c.customer_id = o.customer_id
where o.order_id is null;


Find the second-highest order amount, and explain how you’d handle ties.

with RO as (
    select 
        amount,
        dense_rank() over (order by amount desc) as rnk 
    from orders
)
select distinct amount 
from RO
where rnk = 2;

orders(order_id, customer_id, order_date, amount, status)
customers(customer_id, name, country, signup_date)
order_items(order_id, product_id, quantity, unit_price)
products(product_id, name, category)
employees(emp_id, name, manager_id, salary, dept_id)
logins(user_id, login_date)

select
    c.name,
    coalesce(sum(case when o.status = 'completed' then o.amount else 0 end), 0) as total_completed_spend
from customers c 
left join orders o on c.customer_id = o.customer_id
group by c.customer_id, c.name;

select c.customer_id, c.name
from customers c 
left join orders o on c.customer_id = o.customer_id
where o.order_id is NULL;

with rankedorders as (
    select
        amount,
        dense_rank() over (partition by amount desc) as rnk 
    from orders
)
select distinct amount 
from rankedorders
where rnk = 2;

select
    e.emp_id,
    e.name as employee_name,
    e.salary as employee_salary,
    m.name as manager_name,
    m.salary as manager_salary
from employees e 
join employees m on e.manager_id = m.emp_id
where e.salary > m.salary;

select c.customer_id, c.name
from customers c 
where c.customer_id in (
    select customer_id
    from orders
    where order_date >= '2026-01-01' AND order_date < '2026-02-01'

    intersect

    select customer_id
    from orders
    WHERE order_date >= '2026-02-01' AND order_date < '2026-03-01'
);

select
    c.country
    count(o.order_id) as completed_orders_count
from customers c 
join orders o on c.customer_id = o.customer_id
where o.status = 'completed'
group by c.country
having count(o.order_id) > 5;

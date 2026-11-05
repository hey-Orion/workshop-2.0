Question 2: SQL Coding
Consider the following schema:

orders (order_id, customer_id, order_date, amount, status)
customers (customer_id, name, country, signup_date)

Write a SQL query to show each customers name and their total completed spend (status = 'completed'), 
including customers who have no orders at all (their total spend should show as 0 or NULL).

select
    c.name,
    sum(case when o.status = 'completed' then o.amount else 0 end) as total_spend #
from customers c 
left join orders o on c.customer_id = o.customer_id
group by c.customer_id, c.name;


Lets do a quick follow-up on this before moving to Python:
If you wanted to rewrite this query using a FILTER clause (supported in PostgreSQL/BigQuery) instead of a CASE statement, how would that look?

select
    c.name,
    sum(o.amount) filter (where o.status = 'completed') a total_spend
from customers c 
left join orders o on c.customer_id = o.customer_id
group by c.customer_id, c.name;


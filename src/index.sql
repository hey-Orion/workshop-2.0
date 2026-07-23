select p.category, sum(o.total_amount) as revenue
from orders o 
join product p on o.product_id = p.product_id
where o.status = "completed"
group by p.category
order by revenue desc;

ok i understand this on my quest why import only one table 


select customer_id, count(*) as order_count
from orders 
where status = "sold"
group by customer_id
having count(*) > 5;

just explain this line to me having count(*) > 5;


with ranked as (
    select
        ticket_id,
        status,
        updated_id,
        row_number() over (
            partition by ticket_id
            order by updated_id desc 
        ) as rn 
    from ticket_table
)
i understand this much very well.

select ticket_id, status, updated_id
from ranked 
where rn = 1;
why is this part here explain


# this needs to be fully explaned in detaial
WITH signups AS (
    SELECT user_id, created_at FROM users
),
activated AS (
    SELECT DISTINCT user_id FROM events WHERE event_type = 'activated'
),
paid AS (
    SELECT DISTINCT user_id FROM subscriptions WHERE status = 'active'
)
SELECT
    COUNT(DISTINCT s.user_id) AS total_signups,
    COUNT(DISTINCT a.user_id) AS total_activated,
    COUNT(DISTINCT p.user_id) AS total_paid
FROM signups s
LEFT JOIN activated a ON s.user_id = a.user_id
LEFT JOIN paid p ON s.user_id = p.user_id;


select e.name as employee, m.name as manager
from employees e 
join employees m on e.manager_id = m.employee_id
where e.salary > m.salary;
would need an exp employee_id and manager_id was not selected how can we use it and tell me this means employees with more salary right 
where e.salary > m.salary;


# this needs to be fully explaned in detaial
select  
    DATE_TRUNC("month", u.signup_date) as cohort_month,
    count(DISTINCT u.user_id) as cohort_size,
    count(DISTINCT CASE WHEN u.is_active then u.user_id end) as still_active
from users u 
group by DATE_TRUNC("month", u.signup_date)
order by cohort_month;

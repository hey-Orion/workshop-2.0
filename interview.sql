select 
    customer_id, sum(amount) as total
from orders 
where status = "completed" 
group by customer_id
order by total desc;

select
    u.region,
    count(e.event_id) as login_count 
from users u 
join events e on u.user_id = e.user_id
where e.event_type = 'login'
  AND e.timestamp >= '2026-01-01' 
  AND e.timestamp < '2027-01-01'
group by u.region
order by login_count desc
limit 3;

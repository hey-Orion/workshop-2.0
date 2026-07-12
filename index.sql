select server_name
from datap
where status = "online";

select count(*)
from pipelin_logs;

select * 
from error_logs
where error_code = 500;

SELECT file_name 
from ingested_files 
WHERE loaded_at is NULL;

select job_id
from datad
where status = "failed" and environment = "prod"

select * from server_metrics
order by timestamp asc;

select server_name, count(*)
from error_logs
group by server_name;

SELECT server_name, COUNT(*) 
FROM error_logs 
GROUP BY server_name
having COUNT(*) > 10;


select environment, count(*) as total
from pipelin_logs
where status = "failed"
group by environment
having count(*) > 5;


SELECT servers.server_name, error_logs.error_msg
FROM servers
inner JOIN error_logs why a inner join 
on servers.server_id = error_logs.server_id;


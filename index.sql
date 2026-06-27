explain and decode all these sql quries and tell me what they are doing and why and how 


delete from events
where ctid in (
    select ctid from (
        select ctid,
                row_number() over (partition by event_id order by created_at asc) as rn
        from events
    ) t 
    where t.rn > 1
);

DELETE FROM events
WHERE ctid IN (
    SELECT ctid FROM (
        SELECT ctid,
               ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY created_at DESC) as rn
        FROM events
    ) t
    WHERE t.rn > 1
);
ok what is ctid and created_at i need to look at the table to understand these once


delete from actions
where id in (
    select id from (
        select id,
                row_number() over (partition by user_id, action_type, event_date order by id) as rn
        from actions
    ) t 
    where t.rn > 1
);
why partition by three what dose that do 


with row_to_delete as (
    select id,
            row_number() over (partition by session_id order by logged_at) as rn
    from session_logs
)
delete from session_logs
where id in (select id from row_to_delete where rn > 1);




select event_id, user_id, created_at,
        count(*) over (partition by event_id) as occurrence_count
from staging_events
order by occurrence_count desc;




delete from profiles
where ctid in (
    select ctid from (
        select ctid,
                row_number() over (partition by user_id order by email is NULL, phone is NULL) as rn
        from profiles
    ) t 
    where t.rn > 1 
);




select event_id, user_id, created_at
from (
    select event_id, user_id, created_at,
            row_number() over (partition by event_id order by created_at asc) as rn 
    from staging_events
) clean_data
where rn = 1;



update staging_events
set is_duplicate = TRUE
where ctid in (
    select ctid from (
        select ctid,
                row_number() over (partition by event_id order by created_at asc) as rn
        from staging_events
    ) t 
    where t.rn > 1 
);

delete from servers
where metric_id in (
    select metric_id from (
        select metric_id,
                dense_rank() over (partition by host_id, timestamp order by metric_id) as dr
        from servers
    ) t 
    where t.dr > 1 
);

DELETE FROM transaction_logs
WHERE transaction_id IN (
    SELECT transaction_id FROM (
        SELECT transaction_id,
               ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY created_at ASC, updated_at DESC) as rn
        FROM transaction_logs
    ) t
    WHERE t.rn > 1
);
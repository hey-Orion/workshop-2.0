select
    user_id,
    login_time,
    row_number() over (
        partition by user_id order by login_time
    ) as login_num
from users;


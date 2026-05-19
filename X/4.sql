select c.ticker
from compnies c 
left join trade t 
on c.ticker = t.ticker
where t.ticker IS Null; 


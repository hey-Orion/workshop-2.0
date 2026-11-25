Discussion (two sentences each):What should your code do when an API returns 429, and what does the Retry-After header tell you?

ok so a pipeline or ky pipeline should stop of a short period of time and then retry automatically on the same api not stopping the pipeline completely and the retry after tells us after how long the retry should happen 


Why do retries need idempotent operations? Give an example of what goes wrong when retrying a POST.

so idempotent means running the same pipeline multiple times and getting the same results
we make a pipeline idempotent by usingnon conflict upserts and unique values preventing dublactions in the table 

and without idempotent pipeline a retry can cause  duplicate records leading to wrong calculations and final analysis ready product
### Python

**Q1.** Write a function `get_evens_squared(numbers: list[int]) -> list[int]` that takes a list of integers, filters for even numbers, and returns a list of their squares using a list comprehension.



### SQL

**Q2.** Write a SQL query to select `department_id` and the total salary (`SUM(salary) as total_salary`) from an `employees` table, filtering for departments where `total_salary` is greater than 100,000.



### Pandas

**Q3.** Given a DataFrame `df` with columns `['department', 'salary']`, write a single line of Pandas code to get the median salary for each department.



**Q4.** Given a DataFrame `df`, write a line to replace all missing values (`NaN`) in the `'status'` column with the string `'unknown'`.



### SQLAlchemy

**Q5.** Write a SQLAlchemy query to **delete** all records from the `Pipeline` table where `active == 0` using a `session` object, and commit the transaction.



**Q6.** Write a SQLAlchemy query to fetch the **total count** of records in the `Pipeline` table where `active == 1`.



### Requests

**Q7.** Write a `requests.get()` call to `"[https://api.example.com/data](https://api.example.com/data)"` that includes a custom header `{"Authorization": "Bearer token123"}` and a 5-second timeout, storing the response in a variable `res`.



### Pydantic

**Q8.** Define a Pydantic model `PipelineRun` with three fields:

* `run_id`: integer
* `pipeline_name`: string
* `status`: string with a default value of `"PENDING"`



**Q9.** Write a line of code to parse a JSON string `json_data = '{"run_id": 10, "pipeline_name": "ETL"}'` directly into an instance of `PipelineRun`.



### Pytest

**Q10.** Write a Pytest function `test_pipeline_run()` that uses a mock fixture `sample_run` (which returns a `PipelineRun` instance with `status="PENDING"`) and asserts that its `status` attribute is equal to `"PENDING"`.



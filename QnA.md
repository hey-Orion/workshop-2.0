Conceptual & Architecture Questions

1. Apache Airflow
Question 1: If your daily API data extraction task randomly fails due to network spikes or target maintenance windows in the EU ecosystem, what properties would you set up on your Airflow operators to handle this automatically without waking the team?



Question 2: Explain the difference between Airflow catchup and backfill. What danger occurs if you create a new daily pipeline with catchup=True and a start_date set to one year ago?



2. Docker Compose
Question 1: How do you guarantee your DataOps automation script container does not attempt to execute queries before your database container is fully awake and ready to accept calls inside Docker Compose?



Question 2: What is the fundamental functional difference between mapping a folder via a volume versus a bind mount in a local compose configuration file?



3. GitHub Actions
Question 1: Why is it bad security practice to write plain production database credentials directly inside your repository pipeline configurations, and how do you resolve this inside GitHub Actions?



Question 2: How can you optimize your automated testing pipeline runner to make sure it finishes executing faster on subsequent pull requests?


4. Git / GitHub
Question 1: What is the functional operational difference between running a git command via git merge versus git rebase when pulling updates down from a shared project main branch?



Question 2: A pipeline deployment to production fails immediately because an underlying database dependency was modified. How do you fast-track an environment recovery safely using Git tools?



5. Sentry
Question 1: If you notice your Airflow tasks are failing silently because errors are caught internally by broad try/except statements, how can you configure Sentry to make sure these silent data processing errors are still surfaced?



Question 2: What is Sentry "Issue Grouping" and how does it prevent your operational notification channels from blowing up when a recurring extraction loop breaks thousands of records in a few minutes?



6. Logging
Question 1: When building production-ready automation scripts, what is the problem with using standard Python print() statements instead of using the native logging library?



Question 2: Why should you use logging.exception("Message") inside a Python except code block instead of using a standard message like logging.error("Message")?



7. SQLAlchemy
Question 1: Why is building raw string queries like f"SELECT * FROM users WHERE country = '{user_input}'" highly dangerous, and how does using an engine layer resolve this problem?



Question 2: What does the phrase "Connection Pooling" mean when you configure a backend client using SQLAlchemy's create_engine function?



8. python-dotenv
Question 1: Why should your local environment configuration file .env never be checked into your open Git source repository system?



Question 2: If an environment variable named DB_PORT is set on both your actual host Linux terminal profile and defined inside your local directory .env file, which value takes precedence when load_dotenv() runs?



9. PostgreSQL
Question 1: What is an index in a PostgreSQL database, and what is the operational downside of adding indexes to every single column inside an engineering table store?



Question 2: Explain the difference between an INNER JOIN and a LEFT JOIN in a standard relation table execution.



10. YAML
Question 1: Why does copy-pasting structural code chunks inside YAML configurations frequently cause validation failures, and how do you debug this?



Question 2: In configuration schemas, what is the structural difference between elements declared behind a dash (e.g., - item) versus simple key-value structures?



11. Shell / Bash
Question 1: What does the special pipeline character sequence $? represent in a bash context, and how do you use it inside deployment validation steps?



Question 2: What is the difference between writing output data to a file using a single angular bracket > versus using a double angular sequence >>?



done
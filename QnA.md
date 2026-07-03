50 DataOps Interview Questions

Questions 1–30 (General DataOps – Junior to Mid-Level)

1. Data Pipeline CI/CD

You’re asked to set up a CI/CD pipeline for a data transformation job (e.g., dbt or Spark). What stages would you include, and how would you handle data quality checks before deploying to production?

2. Orchestration & Failure Handling

Imagine a daily Airflow DAG fails halfway because an upstream API returns a 429 (too many requests). How would you design the DAG to recover without manual intervention?

3. Data Versioning & Reproducibility

How do you ensure that a data pipeline run from three months ago can be reproduced exactly? What tools or practices would you use?

4. Monitoring & Observability

What metrics would you monitor for a real-time Kafka-to-ClickHouse pipeline? How would you set up proactive alerts?

5. GDPR & DataOps in the EU

A data pipeline processes personal data of EU citizens. What specific DataOps practices would you implement to support GDPR’s ‘right to erasure’ and data minimization?

6. Schema Evolution

Your upstream source adds a new column to a table. How do you handle this change across downstream transformations and reports without breaking existing views?

7. Infrastructure as Code (IaC) for Data

You need to spin up a dev environment for a data pipeline (storage, compute, orchestration). How would you use IaC to make it reproducible and cost-controlled?

8. Testing Data Quality at Scale

Describe how you’d implement automated data quality tests for a pipeline that processes 10M records daily. What would you test, and where in the pipeline would those tests run?

9. Collaboration & Documentation

In a small DataOps team, multiple people modify pipeline code. How do you avoid conflicts and ensure that data transformations remain documented and understood?

10. Cost Optimisation on Cloud (EU region)

Your pipeline runs on AWS/GCP in eu-west-1. At month-end, costs spike due to excessive data scanning. How would you identify the cause and implement control?

11. Immutable vs Mutable Data

Why is immutability important in a DataOps pipeline? Give an example where mutability would cause a reproducibility issue.

12. Containerising Data Workloads

You need to run a Python data transformation script daily. How would you containerise it (Docker) and integrate it into an orchestrator like Airflow or Prefect?

13. Secrets Management

How do you securely manage database credentials, API keys, and cloud tokens across dev/staging/prod environments in a DataOps pipeline?

14. Alerting & On-Call

Design an alert for a pipeline that processes batch data every hour. What would trigger a page (urgent) vs a Slack message (non-urgent)?

15. Data Lineage

Your manager asks: “Which upstream tables and transformations feed the ‘monthly_sales’ report?” How would you provide this without manual investigation?

16. Retroactive Data Fix

A bug caused wrong values in a fact table for the past 7 days. How do you correct the data, rerun downstream models, and keep audit trails?

17. Environment Parity

Why do pipelines often fail in production after working in staging? What steps would you take to minimise this gap?

18. Handling Late-Arriving Data

Your pipeline runs at 2 AM for yesterday’s data, but some records arrive 3 days late. How do you design the pipeline to handle updates without duplicate or missing data?

19. Data Contract with Source Team

The team that owns the source database changes a column type from INT to STRING. How would you implement a “data contract” to catch this before it breaks your pipeline?

20. Recovery from Data Corruption

Someone accidentally deletes a partition in your production data lake. Walk me through the steps to recover it with minimal downtime.

21. Idempotency in Data Pipelines

What does idempotency mean for a data pipeline? How would you implement idempotent writes to a database or data lake?

22. Blue/Green Deployments for Data

How would you perform a blue/green deployment of a dbt model without causing data inconsistency for downstream consumers?

23. Data Observability Tools

Name three open-source or SaaS data observability tools and describe one metric each would track beyond basic pipeline health.

24. Batch vs Streaming Trade-offs

A business user wants “real-time” dashboards, but the source system is a transactional database. What questions would you ask before deciding on streaming?

25. Data Retention & Archiving

For GDPR compliance, raw event data must be deleted after 30 days. How would you automate this in your pipeline while keeping aggregated reports intact?

26. Parameterising Pipelines

You have the same transformation logic for 10 different clients. How would you parameterise a single DAG/task to avoid code duplication?

27. Error Handling in SQL Transformations

In a dbt model, a LEFT JOIN produces unexpected nulls. How would you add tests and error handling to catch this before production?

28. Resource Optimisation on Kubernetes

Your Spark job runs on a small Kubernetes cluster. What configs (memory, CPU, executor count) would you tune to avoid OOM errors while keeping costs low?

29. Metadata-Driven Pipelines

Your team keeps adding new data sources of the same type (e.g., CSV files from different FTP servers). How would you build a metadata-driven pipeline to reduce new development effort?

30. Final Scenario Question

“Describe a recent DataOps failure you experienced or could imagine. What monitoring, testing, or process change would have prevented it, and how would you implement that change in a new contract role?”

---

Questions 31–50 (Tailored to Dataflow Sentinel / Your Stack)

31. Validation & Optional Fields (Pydantic)

You use Pydantic to validate data before promotion to Silver. How would you extend this to handle optional fields or nullable columns without breaking existing pipelines?

32. Schema Violation Handling

A new upstream source adds a field that violates your Pydantic schema (e.g., string instead of int). Walk me through how your pipeline detects this, logs it, and prevents corrupted data from reaching Gold.

33. Idempotency in Medallion Layers

Your pipeline is designed to be idempotent. How does the Bronze → Silver → Gold promotion guarantee that re-running the pipeline doesn’t create duplicate records? Be specific about your storage write logic.

34. Manual Resume After Failure

If a scheduled run fails at the Silver step, how would you manually resume from that point without re-ingesting Bronze data?

35. Environment Parity (Docker & Makefile)

Your pipeline runs identically locally, in Docker, and in GitHub Actions. What potential environment drift have you observed or prevented? How does your Makefile and .env strategy help?

36. Debugging Docker Dependencies

The Docker container fails because of a missing system dependency (e.g., a C library for yfinance). How would you debug this and update the Dockerfile without breaking other environments?

37. Conditional CI Runs (Cost Optimisation)

Your daily_run.yml workflow runs the pipeline on a schedule. How would you modify it to only run if the source data (Yahoo Finance) has actually updated, avoiding unnecessary compute cost?

38. Diagnosing CI Failures Without Exceptions

You receive a CI email alert that the pipeline failed, but Sentry shows no exception. What steps would you take to diagnose whether it’s a data quality issue, a network timeout, or a resource limit?

39. Custom Sentry Events for Freshness

Sentry captures unhandled exceptions. How would you also send a custom event to Sentry when freshness.json reports "STALE" but no exception is raised?

40. Structuring Sentry Events Without Log Access

Your pipeline runs in a contract role where you don’t have access to production logs. How would you structure Sentry events to include pipeline stage (ingestion, validation, metrics) and data volume metadata?

41. Adding a New Gold Table (Medallion)

A business user asks for a new derived table at the Gold layer. Walk through the steps to add it, ensuring that Bronze and Silver remain untouched and validation still passes.

42. Why Bronze Must Be Immutable

Why is Bronze immutable in your design? Give a concrete example where mutability in Bronze would break the reproducibility of a Silver transformation.

43. Freshness Monitoring – First Checks

Your freshness.json has a status: "STALE". According to your RUNBOOK, what are the first three things you check, and why in that order?

44. Reducing False Freshness Alerts

How would you modify the freshness logic to alert only if data is stale for two consecutive runs, reducing false alarms on market holidays?

45. Storage Abstraction (CSV → PostgreSQL)

You currently write to CSV files. If you had to switch to PostgreSQL for Silver storage, which parts of your code would change and which would stay the same? (Hint: storage abstraction.)

46. Adding an Index Without Changing Pipeline Code

A query on your Gold aggregates is slow. How would you add an index in PostgreSQL without changing your pipeline’s Python code?

47. Orchestration Trade-offs (GitHub Actions vs. Airflow)

You currently orchestrate your pipeline via pipeline.py and GitHub Actions scheduled runs. How would you explain to a CTO the trade-offs between this approach and using a dedicated orchestrator like Airflow or Prefect? When would you recommend switching?

48. Event-Driven Trigger (Webhook / Cron-Check)

Your GitHub Actions workflow runs on a schedule. If you wanted to trigger the pipeline only when a new source file is detected (e.g., a CSV uploaded to an FTP or a webhook from an API), how would you implement that using only your current stack (Python + GitHub Actions + perhaps a simple cron-check)?

49. Selling DataOps to a Small EU E‑commerce Company

Your contract is for a small EU e‑commerce company. They have no dedicated data platform. How would you convince them to adopt your Dataflow Sentinel pattern instead of just running ad‑hoc Python scripts?

50. Ingesting from Google Sheets

The company uses Google Sheets as a source. How would you modify your ingestion module to pull from Sheets, apply the same Pydantic validation, and still follow the medallion layers?

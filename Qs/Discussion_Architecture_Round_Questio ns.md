# Discussion / Architecture Round — Updated Question Set

## Updated Tool List

**High probability — have a real story ready:**
- Apache Airflow
- Docker / Docker Compose
- GitHub Actions
- Logging + Sentry
- PostgreSQL (design/architecture angle, not query-writing)
- Git / GitHub
- **dbt** *(new)*
- **BigQuery** *(new)*

dbt and BigQuery are promoted straight to high-probability, not moderate — you have a real, provable story (the 19 null-`close`-rows investigation, the staging/marts split, the isolation-from-core-pipeline decision), which is exactly what this tier is for.

**Moderate probability — one solid sentence, folds into other answers:**
- python-dotenv
- Makefile
- YAML (via Docker/Airflow/CI/dbt configs)
- bash / Linux / shell

**Low probability — surface-level only, don't over-prepare:**
- AWS/GCP basics (GCP still surface-level — BigQuery is a specific *service* story, not general GCP fluency)
- Networking & Security basics

---

## Data Engineering / Basic Questions (10)

**Q1.** Walk me through what happens to a piece of data from the moment it enters your pipeline to the moment it's queryable.
*→ Narrate Bronze → Silver → Gold → (now also) the Silver → BigQuery export → dbt staging → marts path. Be explicit that Gold and the dbt marts are two separate, parallel outputs of Silver, not a chain.*

**Q2.** Why did you choose a layered (Bronze/Silver/Gold) design instead of writing straight to one clean table?
*→ Fail-fast, debuggability, safe reprocessing from any layer, decoupling ingestion from business logic.*

**Q3.** What's the difference between a data warehouse, a data lake, and a lakehouse? Where does your project sit?
*→ Bronze/Silver as a lake-like raw/cleaned zone on Postgres; BigQuery + dbt as the warehouse layer. Be honest that it's a small, educational version of the pattern, not a true lakehouse.*

**Q4.** How do you ensure a pipeline run is idempotent? Why does that matter?
*→ Layered overwrite strategy, `WRITE_TRUNCATE` in the BigQuery export, deterministic transformations — re-running produces the same result, which matters for safe retries after a failure.*

**Q5.** What's the difference between batch and streaming, and why did you choose batch here?
*→ Market data isn't fetched continuously in your design (scheduled daily runs), so batch fits; streaming would need an always-on ingestion layer and different guarantees (ordering, late data).*

**Q6.** How would you detect a silent data quality problem — one that doesn't throw an exception?
*→ This is your actual story: the 19 null `close` rows. Validation rules, dbt tests catching them as a *count*, not a crash; freshness checks; the principle "silent failures are unacceptable."*

**Q7.** What's a fact table vs. a dimension table? Does your project have either?
*→ Your market data rows are closer to a fact table (one row per symbol/date/metric); you don't really have dimension tables since there's no separate "symbol metadata" table — fine to say so honestly.*

**Q8.** If this pipeline had to scale from 10 tickers to 10,000, what would break first and what would you change?
*→ Probably ingestion rate-limiting and Postgres write volume first; discuss batching API calls, maybe moving to a queue, partitioning BigQuery tables by date.*

**Q9.** How do you decide what to test vs. what to just monitor in production?
*→ Tests (pytest, dbt tests) catch known, expected failure modes before/during a run; monitoring (Sentry, freshness.json, Airflow UI) catches the unknown unknowns at runtime. Both are needed.*

**Q10.** What's one thing you'd do differently if you rebuilt this project from scratch?
*→ Have a genuine, specific answer — e.g. "I'd design the Silver schema with the warehouse export in mind from day one instead of bolting it on later," or similar. Avoid a generic non-answer like "nothing."*

---

## Apache Airflow (5)

**Q1.** What's the difference between a DAG, a Task, and an Operator?
*→ DAG = the whole workflow graph; Task = one node/unit of work; Operator = the template/class that defines what a task actually does (PythonOperator, BashOperator, etc.).*

**Q2.** Where does Airflow store task state and XComs, and why does that matter?
*→ The metadata database (Postgres in your setup), not in memory — this is why Airflow survives scheduler restarts and why tasks can be inspected after the fact.*

**Q3.** What happens if a task fails halfway through a DAG run? Walk me through your recovery process.
*→ Your actual runbook: inspect the task log, fix root cause, clear the failed task + downstream tasks, rerun. Airflow re-executes only the cleared tasks, not the whole DAG.*

**Q4.** Why use Airflow instead of just running a Python script on a cron schedule?
*→ Visibility (UI, logs, retry history), dependency management between steps, retry logic, and it scales to more complex multi-step pipelines than cron reasonably can.*

**Q5.** What's the difference between `start_date` and `catchup`, and why do they matter operationally?
*→ `start_date` sets when the DAG logically begins; `catchup=True` would backfill every missed interval since then on first activation — a common footgun that causes a flood of unwanted historical runs if left on by accident.*

---

## Docker / Docker Compose (5)

**Q1.** Why containerize this pipeline at all, given it already runs fine locally?
*→ Environment parity — eliminates "works on my machine," guarantees the same Python/OS/dependency versions in CI, local, and (if deployed) production.*

**Q2.** What's the difference between a Docker image and a container?
*→ Image = the built, immutable template; container = a running instance of that image.*

**Q3.** What's a bind mount and why would you use one during development?
*→ Maps a host folder into the container live, so code changes are reflected without rebuilding the image — useful in dev, risky/avoided in production for reproducibility.*

**Q4.** Why might you split services into multiple containers (e.g. Airflow webserver, scheduler, Postgres) instead of one big container?
*→ Separation of concerns, independent scaling/restarts, and it mirrors how these components would actually be deployed in production.*

**Q5.** What's the purpose of a `.dockerignore` file, and what's a real mistake you've made with one?
*→ Keeps build context small and prevents secrets/junk from landing in the image. Your real story: you once had `warehouse_export/` excluded, which would've silently kept real source code out of version control — a good, honest example of catching your own config mistake.*

---

## GitHub Actions (5)

**Q1.** Walk me through what your CI workflow actually does, step by step.
*→ Triggered on push/schedule/manual dispatch → runs tests via pytest → runs the pipeline → sends email alert on success/failure.*

**Q2.** What's the difference between a scheduled run and `workflow_dispatch`?
*→ Scheduled = cron-based automatic trigger; `workflow_dispatch` = manual, on-demand trigger you click in the GitHub UI — useful for re-running after fixing an incident.*

**Q3.** Why run tests *before* running the pipeline in CI, rather than after or not at all?
*→ Fail fast — no point executing (and potentially writing bad data from) a pipeline you already know is broken.*

**Q4.** How do you handle secrets (DB credentials, API keys) in a GitHub Actions workflow?
*→ GitHub Actions encrypted secrets, injected as environment variables at runtime — never hard-coded or committed.*

**Q5.** What would you do if a workflow passed in CI but failed when triggered by Airflow?
*→ Investigate environment-specific differences — different env vars injected, different working directory, different Postgres environment target (Neon vs local), since your `make test`/`make docker_test` local-repro step is specifically designed to catch or rule this out.*

---

## Logging + Sentry (5)

**Q1.** What's the difference between what you'd put in a log file versus what you'd want Sentry to capture?
*→ Logs = full execution trace, expected and unexpected events, for later audit; Sentry = specifically unhandled exceptions with stack trace + environment context, for real-time alerting.*

**Q2.** Where is `SENTRY_DSN` configured, and what happens if it's missing?
*→ Environment variable; if absent, monitoring stays disabled — a deliberate safe-default so local dev doesn't require a Sentry account.*

**Q3.** Why initialize Sentry at the very start of `pipeline.py` rather than inside individual modules?
*→ So it's active before any downstream code runs — otherwise an early failure (e.g. in ingestion) could go uncaptured.*

**Q4.** What's a "silent failure" and how does your design prevent one?
*→ A failure that doesn't crash or alert anyone — e.g. an empty dataset silently "succeeding." Prevented by validation checks, freshness checks, and explicit status reporting rather than assuming no exception means success.*

**Q5.** If Sentry shows no events but the pipeline clearly failed, what would you check?
*→ Whether `SENTRY_DSN` is actually set in that environment, whether monitoring initialization ran before the failure occurred, and whether the failure was actually handled/swallowed somewhere instead of raised.*

---

## PostgreSQL — design/architecture angle (5)

**Q1.** Why Postgres for this project instead of, say, SQLite or a NoSQL store?
*→ Relational structure fits tabular market data well; strong consistency guarantees; mature tooling (SQLAlchemy); Neon gives you managed hosting without running your own instance.*

**Q2.** What would you do if you saw schema drift between what your code expects and what's actually in the table?
*→ Compare the SQLAlchemy model/migration definitions against the live table, check for manual changes, and add stricter validation or migrations going forward to prevent silent drift.*

**Q3.** How do you think about connection pooling in a pipeline that runs on a schedule, not continuously?
*→ Scheduled batch jobs don't need a large persistent pool like a web app would — open connections for the run, close them cleanly afterward, which is what your `run_export()`-style functions already do.*

**Q4.** What's the risk of running the same pipeline against both a local Postgres (Docker) and a remote Neon instance?
*→ Config/credential mixups, different latency profiles, potential version differences — mitigated by your environment-variable-driven config and the explicit environment mapping (local/Docker/CI/Airflow → which Postgres).*

**Q5.** If this table grew to hundreds of millions of rows, what's the first architectural change you'd consider?
*→ Partitioning by date, archiving old data out of the hot table, possibly moving historical data entirely into the warehouse (BigQuery) and keeping Postgres lean for recent/operational data only.*

---

## Git / GitHub (5)

**Q1.** What's your branching strategy on this project, even if it's a solo project?
*→ Honest answer is fine — e.g. mostly direct commits to main for a solo project, but you understand feature-branch workflows for team settings; show you know *why* teams use them (isolation, PR review) even if you don't need it solo.*

**Q2.** What's the difference between `git merge` and `git rebase`, and when would you use each?
*→ Merge preserves full history with a merge commit; rebase rewrites history onto a new base for a cleaner, linear log — rebase is riskier on shared/public branches.*

**Q3.** How do you keep secrets out of a public GitHub repo?
*→ `.gitignore` for `.env*` files, never committing keys, using GitHub Secrets for CI — and your own real example of catching a `.gitignore`/`.dockerignore` bug before it caused a leak or a code-exclusion problem.*

**Q4.** What would you do if you accidentally committed a secret to git history?
*→ Rotate/revoke the credential immediately (most important step), then remove it from history (e.g. `git filter-repo` or BFG) — rotating matters more than scrubbing history since it may already be cached/forked.*

**Q5.** What's in your `.gitignore` for this project, and why those specific entries?
*→ `.env*` (with example-file exceptions), `.gcp/` (service account keys), venv folders, dbt's `target/`/`dbt_packages/` — each tied to a real reason (secrets, build artifacts, local-only state).*

---

## dbt (5)

**Q1.** Why add dbt on top of a pipeline that already has a Gold layer? Isn't that duplicating work?
*→ It's not duplication — Gold is a run-time-only artifact from the Python pipeline; the dbt marts (`daily_returns`, `volatility`, `ma_crossover`) are new analytics that didn't exist before, built on data landed in BigQuery, explicitly isolated from the core pipeline's reliability guarantees.*

**Q2.** What's the difference between a dbt source, a staging model, and a mart model in your project?
*→ Source = the raw landed table (`raw_market_data`) declared in `sources.yml`; staging (`stg_market_data`) = casts/renames/filters nulls; marts = the actual business logic (returns, volatility, crossover) built on top of staging via `ref()`.*

**Q3.** Walk me through the null `close` data quality issue you found — what happened and how did you resolve it?
*→ Your real story: `dbt test` failed with 19 null-close rows in the source; you investigated in BigQuery, found a pattern (same 6 dates across multiple tickers, consistent with a same-day fetch timing gap); resolved by removing the `not_null` test from the *source* (documented as a known, accepted exception) since the real guarantee is already enforced downstream in staging (`WHERE close IS NOT NULL`).*

**Q4.** What does `ref()` actually do, and why does it matter for dependency management?
*→ It builds the dependency graph between models automatically and makes model names environment-agnostic — dbt figures out build order and which dataset/schema to point to, so you never hardcode a table name across models.*

**Q5.** This dbt layer isn't wired into Airflow or GitHub Actions yet — why not, and what's the risk of leaving it that way?
*→ Honest answer: it's a deliberately separate, currently-manual layer so it can't break the core pipeline's reliability guarantees while still being developed. Risk: it can silently go stale since nothing alerts on it yet — which is exactly why it's flagged as a documented future improvement, not an oversight.*

---

## BigQuery (5)

**Q1.** Why BigQuery specifically, instead of just running these analytics queries directly against Postgres?
*→ Columnar storage suited to analytical aggregation queries, decouples analytics workload from the operational database, and gives you a realistic "warehouse" layer to practice the pattern most EU/UK DE roles actually use.*

**Q2.** How does data actually get from Postgres into BigQuery in your setup?
*→ A dedicated export script (`warehouse_export/export_to_bigquery.py`) reads the Silver table from Neon, then loads it into BigQuery using `WRITE_TRUNCATE`, landing in a raw table that dbt then sources from.*

**Q3.** What does `WRITE_TRUNCATE` do, and why did you choose it over append?
*→ It replaces the entire destination table on each load rather than appending — appropriate here because the export reflects the full current state of Silver, not an incremental delta; append would duplicate rows on every re-run.*

**Q4.** What IAM roles does your service account need, and what happened when one was missing?
*→ BigQuery Data Editor (write access) and BigQuery Job User (permission to run query jobs) — your real debugging story: `dbt debug` failed with an Access Denied error because only Data Editor had been granted; adding Job User fixed it.*

**Q5.** What's a practical limitation of using BigQuery's sandbox/free tier, and how did it affect your setup?
*→ No billing enabled means certain features and higher quotas aren't available; you worked within the free-tier constraints, which is a normal real-world trade-off to be upfront about rather than oversell.*

---

## python-dotenv (5)

**Q1.** What problem does python-dotenv actually solve?
*→ Loads environment variables from a `.env` file into the process at runtime, so config/secrets don't have to be hardcoded or exported manually in every shell session.*

**Q2.** Why do you have multiple `.env` files (`.env`, `.env.airflow`, `.env.dbt`) instead of one?
*→ Different execution contexts need different overrides (e.g. Airflow's internal network hostnames vs. local `localhost`), so splitting keeps each environment's config explicit and non-conflicting.*

**Q3.** What's a security risk with `.env` files, and how do you mitigate it?
*→ Accidentally committing one to git; mitigated via `.gitignore` entries for `.env*`, with explicit exceptions only for `.env.example`-style template files.*

**Q4.** Does `.env` work the same way in Docker as it does locally?
*→ Not automatically — Docker Compose needs an explicit `env_file:` directive or `environment:` block; dotenv loading inside the app doesn't reach into the container unless the file is actually present/mounted there.*

**Q5.** What would you do differently for secrets management in a real production environment vs. `.env` files?
*→ Use a managed secrets service (e.g. GCP Secret Manager, AWS Secrets Manager) injected at deploy time rather than files on disk — `.env` is fine for solo/dev projects but not a production-grade secrets strategy.*

---

## Makefile (5)

**Q1.** Why wrap commands in a Makefile instead of just documenting raw commands in the README?
*→ Reduces friction and typos, gives a single consistent interface (`make run`, `make test`) regardless of the underlying command's complexity, and self-documents available operations via `make help`-style targets.*

**Q2.** Walk me through what `make docker_all` actually does under the hood.
*→ Be ready to state the real underlying docker-compose/build/run commands it wraps — don't just say "it runs docker," know the actual steps.*

**Q3.** What's a `.PHONY` target and why does it matter?
*→ Tells Make the target isn't a real file, so it always runs the recipe instead of skipping it if a file with that name happens to exist — important for targets like `test` or `clean`.*

**Q4.** How do you pass environment-specific variables through a Makefile target?
*→ Via shell environment variables, `.env` sourcing, or Make variables (`make run ENV=production`) depending on how the target is written — be ready to describe which style your own Makefile uses.*

**Q5.** What's a limitation of Makefiles compared to a proper task runner for larger projects?
*→ No built-in dependency resolution across non-file targets, limited cross-platform support (Windows), and it doesn't scale well to large parameterized pipelines — fine for a project this size, not infinitely scalable.*

---

## YAML (5)

**Q1.** Where does YAML show up across your project, and why that format specifically in each case?
*→ `assets.yaml` (config), Docker Compose files, GitHub Actions workflows, dbt's `sources.yml`/`schema.yml` — chosen because it's the native config format each of those tools expects, not something you picked yourself.*

**Q2.** What's a common YAML bug that's bitten you or could easily bite someone?
*→ Indentation errors (YAML is whitespace-sensitive), and the classic "Norway problem" (unquoted `no`/`yes` being parsed as booleans) — good to mention even if it hasn't hit you directly.*

**Q3.** What's the difference between a list and a mapping in YAML, and how does that show up in a GitHub Actions workflow?
*→ A mapping is key-value (`steps:` containing named keys); a list is `-`-prefixed items (each step in a job's step sequence is a list item that's itself a mapping).*

**Q4.** Why does dbt use YAML for `sources.yml` and model tests instead of just more SQL or Python?
*→ Declarative config separates "what should be true about this data" (tests, descriptions, column metadata) from "how to transform it" (the SQL in the model files) — keeps intent and logic cleanly separated.*

**Q5.** How would you validate a YAML file is well-formed before it causes a runtime failure?
*→ A YAML linter, or simply trying to parse it with `yaml.safe_load()` in a quick script/test — catching syntax errors before they surface as a confusing downstream tool error.*

---

## bash / Linux / shell (5)

**Q1.** What's the difference between `>` and `>>` in shell redirection?
*→ `>` overwrites the target file; `>>` appends to it — easy to mix up and lose log history by accident.*

**Q2.** How would you check if a process (like the Airflow scheduler) is actually running?
*→ `ps aux | grep <process>`, or checking via `systemctl status` / `docker ps` depending on how it's deployed.*

**Q3.** What's the difference between a shell script's exit code 0 and non-zero, and why does CI care?
*→ 0 = success, non-zero = failure; GitHub Actions treats any non-zero exit as a failed step, which is how your pipeline run or test suite failing actually halts/flags the workflow.*

**Q4.** What's the difference between `$PATH` and a shebang line (`#!/bin/bash`) at the top of a script?
*→ `$PATH` tells the shell where to look for commands by name; a shebang tells the OS which interpreter to use to execute the script file itself, independent of `$PATH`.*

**Q5.** How would you debug a script that behaves differently when run via cron/Airflow vs. run manually in your terminal?
*→ Usually environment differences — a non-interactive shell may not load the same `.bashrc`/env vars/`$PATH`; check what environment variables are actually present in that context versus your interactive shell.*

---

## AWS/GCP basics (5)

**Q1.** What's the rough equivalent of an IAM role in AWS vs. GCP?
*→ AWS IAM roles/policies vs. GCP IAM roles/service accounts — same underlying concept (permissions granted to an identity), different terminology and structure.*

**Q2.** What's a service account, and how is it different from a regular user account?
*→ A non-human identity used by an application or script to authenticate to cloud services — what your dbt/BigQuery export script actually authenticates as, via a JSON key file.*

**Q3.** What's the difference between object storage (S3/GCS) and a managed database service?
*→ Object storage holds unstructured files/blobs cheaply at scale; a managed database (Cloud SQL, RDS) provides structured, queryable, transactional storage — different tools for different access patterns.*

**Q4.** Why might a company choose a managed service (like BigQuery or RDS) over self-hosting the equivalent open-source tool?
*→ Reduced operational burden (patching, scaling, backups) at the cost of some control and potential vendor lock-in — a classic build-vs-buy trade-off.*

**Q5.** What's a region/zone in cloud infrastructure, and why might it matter for a project like yours?
*→ Region = geographic location of resources; zone = isolated location within a region. Matters for latency and for your actual BigQuery dataset location requirement (EU consistency) you had to satisfy during setup.*

---

## Networking & Security basics (5)

**Q1.** What's the difference between a public and a private subnet?
*→ Public subnet has a route to the internet (via an internet gateway); private subnet doesn't — databases/internal services typically sit in private subnets, not exposed directly.*

**Q2.** What's a VPC, in plain terms?
*→ An isolated virtual network within a cloud provider where your resources live, with its own IP ranges and routing rules, separate from other tenants' networks.*

**Q3.** Why shouldn't a database be directly exposed to the public internet?
*→ Attack surface reduction — every open port/service is a potential entry point; access should go through authenticated, limited channels (app layer, VPN, private networking) instead.*

**Q4.** What's the difference between authentication and authorization?
*→ Authentication = proving who you are (login, API key, service account key); authorization = what you're allowed to do once authenticated (IAM roles/permissions).*

**Q5.** What's HTTPS actually protecting against, at a basic level?
*→ Encrypts data in transit so it can't be read or tampered with by someone intercepting the connection — relevant to your own `requests` calls to external APIs and your own data staying encrypted in transit to BigQuery/Neon.*

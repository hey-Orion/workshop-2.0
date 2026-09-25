Track 2 — Discussion: Fix yesterday's gaps

Why does a DAG have to be acyclic:
"A DAG has to be acyclic because if there were a cycle — say Task A depends on Task B, and Task B also depends on Task A — the scheduler would have no valid starting point and no way to determine when the pipeline is actually finished. It couldn't compute any order that satisfies both dependencies at once, so it would just loop indefinitely. The 'acyclic' property is what guarantees Airflow can always calculate a clear, deterministic execution order from start to finish."

Why teams avoid committing directly to main:
"Teams avoid committing directly to main because it's meant to represent the stable, production-ready version of the code. If everyone pushed straight to main, an untested or broken change could break the live pipeline immediately. Using feature branches means each change gets reviewed and tested in isolation first — through a pull request — before it's merged into main. That protects the team from unexpected crashes or downtime in production."

bind mount maps you host machine path to the docker contaner   

the actual reasoning 
(code review, testing safety, protecting a stable production branch from untested changes)
these are the main reasuns why we use a main and a featured branch


Track 3 — Salary rehearsal + first full mock

Write your own salary/logistics answer, in your own words, stating €40k and remote/on-site flexibility plainly, no hedging.

im harsh a data engineer right now im expolring eu/uk oportunites about my backgroud im a self taught data engineer i start from devops then though out my learning curve i shifted to data engineering buecous i found it more enjoyable to work with data.
and becouse of it i know the basics of devops lifecycle ae well for you to asses my skills this is my portfoilo project Dataflow-Sentinel its a data pipieline project fully automated and deployed on github actions and airflow

now the salary/logistics answer
for this role my main focus on remoate work but im comfotable with on-site alse but with the condation of sponser and visa
and for my requirments there are none i just want good working hours thats it.
and for the salary part my minimum requirment is €40k if remote but if you require me on-site then i would require the salary as per the sataders.
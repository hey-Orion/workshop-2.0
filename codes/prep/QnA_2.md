Track 2 — Discussion: GitHub Actions, Logging/Sentry, Git/GitHub

What is a GitHub Actions workflow, and what triggers it?

a github action workflow is a automated corn orcastrated for your project in the github you can trigger it wiht cron or on push or manually 
the adv is its free but with some limits basically think of it as a cicd tools build in github

What's the difference between a GitHub Actions "job" and a "step"?

ok so in a workflow file we define task as jobs like test run install etc and steps are the the commands, paths, opratores inside the jobs.

In your CI/CD setup, what does your pipeline actually check before code gets merged/deployed?

right now at each run it tests the code first and then run it as it should. because its triggerd by cron right now but i can make it so test the code at evey push to main like people do in production.

Why use a dedicated tool like Sentry instead of just writing errors to a log file?

loggs file are good but if you want quick and fast error location the sentry takes the win it can pin point the error instently making debugging fast and easy 
also it got an error elert system in it so if the pipelin errors i will get a notifyed instently

What's the difference between logging levels like INFO, WARNING, and ERROR — and how did you decide what to log at each level in your project?

so log levels are use to lable what kind of messege is in logs like info is for basic info about the run the warning is for if a process it taking time or test failed or somthing is wrong but nothing major and error is for if something happend like no data found or db is not responding or the assets are missing there is a level caulld critical too its for somthing major like a data leak. 

What's the difference between git merge and git rebase?

git merge mergase the main and the freture branch togather keeping the seprate commit history by creating a new commit we mostly do merge after testing the code in a feature branch and rebase takes the featuere branch and commits it in the front of the main branch it dose not keep the history of feature branch.  

What's the difference between main and a feature branch in your normal workflow — and why do teams avoid committing directly to main?

so in my case i only use one brance main because its a persnal potfilo project but in prod we should always use feature branches because evey commit or code change should be tests and reviewd before pushing to the main branch to prevent unexpted errors creshes of the pipeline and to keep our existing pipleine running healthy and stable with low to none down time.


Track 3 — Project Walkthrough

What the pipeline does, in one clear sentence (this is the piece to fix from yesterday)
Why Medallion Architecture (Bronze/Silver/Gold) — what problem does that layering solve
Why Airflow (tie back to your migration story)
One technical challenge you hit and solved (Docker/WSL2, or another)
What you'd add next if you had more time (shows forward thinking) 

so Dataflow-Sentinel is a data pipeline oprating on a api data source (yfinance) it takes the raw data and transforms it into anylatics ready records
for the transofmation process im useing the medallion archtecture here it seprets the data transformation in three difftent layers making it easy to transform data, implement chages and error handling because of the sepration the broze layes holds the raw fetched data the silver layer hold the transformad and cleaned data and the gold layer holds the anylatics ready records for predactions and market reserchs etc the transformation happends bettween layers 
the project is deployed in four envourmetns = github actions, docker, local, airflow. also got sentry for error handling.
the reason i chose airflow is becous its retry, and ui dashboard with all the info about the pipeline and active logging properties which github and local deployment dont provide.
i had few techinical chalanges with this project but the one i remember is it was with docker 
i issue was it was not working inside the docker becouse of dependce issue and the host issue i had the postgres db in local and becouse of the there the conn issue happning caus the db was in windows and the docker was in linux to solve these problem i shifeted the db to cloud db sloving the conn issue with the and the dependies issue with the is currect dependice versions.
if i had more time i would shifted the project to cloud (aws) and  add more tickers also i would store the logs to a cloud log storage and add a data dashbord like grifana.

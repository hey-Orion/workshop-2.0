# Basic Interview Questions and Tips — Tailored for You

For entry-level remote EU/UK Data Engineer / Analytics Engineer / BI / Data Analyst (technical) / ETL roles. Each question has guidance on what to say, using your real project and background. Write your own answers in your own words, say them out loud, and keep them to 30-90 seconds unless it's the project walkthrough.

Rule for every answer: only claim what is true and provable from your project. If you don't know, say what you'd do to find out.

---

## 1. About You

**1. Tell me about yourself.**
Use past, present, future in about 60-90 seconds.
- Past: self-taught, built data skills from scratch without a degree.
- Present: built Dataflow-Sentinel, a production-style pipeline (Bronze/Silver/Gold, Airflow, Docker, GitHub Actions, Sentry, plus a dbt/BigQuery analytics layer).
- Future: looking for a first data engineering role where you can build reliable pipelines on a team.
- Don't start with your childhood or list every tool.

**2. Why data engineering?**
Give a real reason in two sentences, such as liking the problem of making data reliable and trustworthy. Tie it to something you did in the project, like catching bad data before it spreads.

**3. Walk me through your CV.**
Go in order, one line per section, and spend most of the time on the project. Know every number on the page. Fix the resume/cover letter mismatch (7 tickers and ~11,000 records versus 10 tickers and ~19,000+) before any interview.

**4. What are your strengths?**
Pick two that you can prove: for example, debugging data-quality problems methodically, and building things so they fail loudly instead of silently. Back each with one example from the project.

**5. What is your biggest weakness?**
Be honest and show you're fixing it. A true one for you: you're slower at writing code from memory under pressure than at reasoning about it. Say what you're doing about it: daily cold drills, a syntax log, and mock interviews.

**6. Why should we hire you?**
Three points: you build reliable, tested pipelines, you learn quickly and fix your own mistakes, and you work independently as a remote worker. Then connect one point to something in their job post.

---

## 2. The Job and the Company

**7. Why do you want this job / this company?**
Say one specific thing about their product, data stack, or work, found in the job post, their website, or an engineering blog. Avoid empty phrases such as "industry leader."

**8. What do you know about us?**
Spend 10 minutes before each interview on what they sell, who their customers are, and what their data stack probably looks like. Say it in two sentences.

**9. What are you looking for in your next role?**
A team where you can learn from experienced engineers, work on real pipelines, and take ownership over time. Keep it specific and honest.

**10. Where do you see yourself in 5 years?**
A solid engineer who owns pipelines end to end and is learning system design and scale. Don't promise to stay forever, and don't say "your job."

---

## 3. Your Project (the main event)

**11. Walk me through Dataflow-Sentinel.**
Prepare a 3-minute version: the problem (silent data failures), the architecture (Bronze → Silver → Gold), how it runs (Airflow, Docker, GitHub Actions), how it's monitored (Sentry, freshness check), and the analytics layer (Silver exported to BigQuery, dbt models on top). Practice it out loud until it's smooth.

**12. Why did you design it this way?**
Layers for debuggability and safe reprocessing, validation before promotion, idempotent re-runs. Be ready to say what you'd change.

**13. What was the hardest problem you hit?**
Pick one with a clear story. Strong options:
- The 19 null `close` rows: dbt test failed, you investigated in BigQuery, found the same 6 dates across tickers, and fixed the test placement instead of hiding the problem.
- The IAM error: `dbt debug` failed until the service account also had BigQuery Job User.

**14. Tell me about a mistake you made.**
Use a real one: you assumed Gold was a Postgres table and built an export for it, then corrected it when you checked how the pipeline actually works. Say what you learned, which is to verify assumptions against the real system first.

**15. How do you make sure your data is correct?**
Pydantic validation at entry, tests (pytest and dbt tests), freshness checks, and alerts. Mention that you chose to keep the dbt layer separate so it can't break the core pipeline.

**16. What would you improve or do next?**
Wire the dbt layer into Airflow or CI, add alerting for it, and add more observability. This also shows you know the project's limits.

**17. How did you test it?**
pytest covers ingestion, validation, storage and metrics, and dbt tests cover the analytics layer. Be honest about what isn't covered.

---

## 4. Behavioral Questions (use STAR with your project)

STAR = Situation, Task, Action, Result. Keep each to about 60-90 seconds.

**18. Tell me about a time you solved a hard problem.** Use the null `close` rows.

**19. Tell me about a time you failed or got something wrong.** Use the Gold-layer assumption or the `.gitignore` bug.

**20. Tell me about a time you learned something quickly.** Use setting up dbt and BigQuery from scratch.

**21. How do you handle feedback or being corrected?** Say how you responded when your assumptions were corrected, and what you changed.

**22. Tell me about working in a team or with others.** You don't have a work team, so be honest: say you've worked mostly independently, and describe how you use code review habits, documentation (README, ARCHITECTURE, RUNBOOK) and clear commits so others could work with your code. Don't invent a team.

**23. How do you handle a deadline or too much work?** Describe how you prioritize and break work into small pieces, using your structured daily routine as the example.

**24. Describe a time you disagreed with someone.** If you don't have a work example, use a technical decision you reconsidered after testing it, or say plainly that you don't have a direct example and describe how you'd handle it.

---

## 5. The Hard Ones (prepare these in advance)

**25. You have no degree and no work experience. Why should we trust you can do this job?**
Stay calm and factual. Self-taught, built and shipped a working pipeline, can show the code, tests, docs and runbook, and can learn fast. Offer to do a technical exercise. Don't apologize or get defensive.

**26. Why are you applying to remote jobs in Europe from India?**
Honest and practical: you want a remote role, you can work overlapping CET/CEST hours, and you're ready to be reliable with communication. Know your visa/contract situation and state it plainly.

**27. Are you comfortable working in our time zone?**
Say yes only if it's true. Name the hours you can work.

**28. Contractor or employee?**
Know what you're open to. Many remote EU/UK roles for people in India are contractor-based, so be ready to talk about invoicing and availability.

**29. What are your salary expectations?**
Give a range and tie it to the market: for example, "€40-50k depending on the scope of the role." Don't say "whatever you think." If they ask first and you're unsure, ask what range the role has budgeted.

**30. When can you start?**
Answer with your real availability.

**31. Do you have other offers or interviews?**
Be honest. "I'm interviewing with a few companies" is enough, with no pressure tactics.

---

## 6. Basic Technical Discussion

Short, clear answers. See your discussion-round file for fuller guidance.

**32. What's the difference between Bronze, Silver and Gold layers?**
**33. What does idempotent mean, and why does it matter?**
**34. What's an Airflow DAG, task and operator?**
**35. Why use Docker for a pipeline?**
**36. What's the difference between ETL and ELT?**
**37. What is a data warehouse versus a data lake?**
**38. What does dbt do, and why did you add it?**
**39. How would you detect bad data that doesn't throw an error?**
**40. What happens if your pipeline fails halfway through?**

---

## 7. Questions to Ask Them (always ask 2-3)

1. What does the data stack look like, and what tools does the team use today?
2. What would success look like in the first 90 days?
3. How does the team handle code review and onboarding?
4. What's the biggest data problem the team is working on right now?
5. What are the next steps in the process, and when should I expect to hear back?
6. Is this role employee or contractor, and what does the working-hours expectation look like? (Ask this if they haven't already said.)

Don't ask about salary or holidays in the first call unless they raise it.

---

## 8. Tips

**Before**
- Spend 10 minutes on the company. Read the job post twice and note 3 matching skills.
- Rehearse your intro, project walkthrough and three stories out loud.
- Test your camera, microphone, internet and lighting. Keep a backup connection ready.
- Have a glass of water, a notepad and your resume open, but not your notes on screen.

**During**
- Greet them warmly and keep it professional.
- Listen to the full question, then pause for a moment before answering.
- Keep answers to 1-2 minutes. If they want more, they'll ask.
- When you're stuck on a coding question, say your approach out loud, start with the simplest version, then improve it.
- If you don't know something, say "I haven't used that, but here's how I'd approach it."
- Be honest. Don't claim tools you haven't used.

**After**
- Send a short thank-you email within 24 hours, mentioning one thing you discussed.
- Write down every question you were asked and where you struggled, then add those to your drills.
- If you're rejected, reply politely and ask for feedback once. Many won't answer, but the ones that do are valuable.

**Practice routine**
- Say 3 answers out loud every day, such as the intro, one project question and one behavioral story.
- Record yourself once a week and listen for filler words and rambling.
- Do one watched mock session a week (a friend or Aced Practice).

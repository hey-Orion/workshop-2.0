### Discussion (answer out loud or in two or three sentences):

What are Bronze, Silver and Gold layers, and why use them?

we need this arcitucherso we can isolate then proceses making it easy to debug and find errors in the pipeline 
the bronze layer contanes the row data, the silver contanes the cleaned and filtered data and the gold layer have the final product 

What’s the difference between a Docker image and a container?

the docker contaner runs on the images 
and images is a templete for multipal comtaners you can run multipal contaners with a single images 

What does “idempotent” mean for a pipeline? 

idempotent mean for a pipeline if it runs multiple times it should give the same result with no duplicats we can prevent that by using uniques values. 

What is a DAG in Airflow?

a dag is what our pipeline runs in it help to run our pipeline in order alse gives a dashbort for the piprline in the airflow ui

What is a primary key, and why does every table need one?

primary key is a unique value in the table. we need it to pin point a row for analysis and to prevent dublicated records 

What do the E, T and L in ETL stand for, and what happens in each step?

so etl stands for extract transform and load 
in extract we collect or get the data from an api.
in transform we clean and transform the data feched by the extrach layer without saving it 
the we take that cleaned data and load it in our db in the load layer 


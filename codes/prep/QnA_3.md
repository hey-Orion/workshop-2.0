befoe i re wirte the codes here are the track 2, 3
im answering in short becous of lack to time right now so the answers are going to be shallow 

What's the difference between database normalization and schema versioning?

db normalization is a fixed schema version for the db that, that will be default of table and schema versinoning is like versions of data bineg stored on db so we can go back and forth without any major chages 

What is data lineage, in your own words?

data lineage is like a history of data what has been stored form the start to now 

What's the difference between streaming and batch processing?

streaming is like data bieng procesed in a stream like without any stages form api to dashbort with less delay and diract proeces  and batch processing is processing data in stages 

What's the difference between a fact table and a dimension table?

fact table is for bussines data like integers and keys and dimesion tables is for descraption data like a product data 

What's the difference between a data warehouse, a data lake, and a lakehouse?

data lake contanes the raw uncleaned data and lakehoues has the mix of raw and clened data and data warehouse has cleaned and struchered data 

What's the difference between a public subnet and a private subnet?

public subnet is accsebal to peplen has ip and open inbound and outbound and privet subnet is oposite its mustly used inside compnies 

Where does Airflow actually store XComs — is it in memory, or somewhere else?

its genraly in temp memory to talk between tasks 

What's the relationship between master and main as branch names?

main is for the final code which runs then project and master is for testing new updates for the project 



Makefile → Airflow migration — what was the situation before (manual make commands), what was the task/goal, what actions did you take, what was the measurable result (e.g., 5 commands → 1)?

Docker/WSL2 debugging incident — pick the one consistent version of this story we flagged yesterday (path translation vs DB connectivity — or both, but know which is the headline), and structure it S-T-A-R.

so the reasion to shift from make to airfow is to automate the project deployments and some other features like auto retires and a project info dashbord with log and timing etc 

so the issue was when i try to run the project in docker the paths and local postgres was causing the errors i solved them by shifting the db to cloud (neon)
and currected the paths throught shifted the rpoject the a linux env  form windws env 

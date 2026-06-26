FROM python:3.11-slim

WORKDIR /app

COPY requirments.txt . 

RUN pip install -r requirments.txt

COPY . . 

CMD [ "python","main.py" ]


Why should you use a specific minor version tag like python:3.11-slim instead of just writing FROM python:latest?

becouse the latest version is genrally unstable and we wirte slim to keep the image light  

What does the environment variable ENV PYTHONUNBUFFERED=1 actually do, and why is it critical for viewing logs in Docker/Airflow?

PYTHONUNBUFFERED makes the print and error messeges appear faster for easy dubbging 



.PHONY: install test run up down 

install:
	pip install -r requirments.txt 

test:
	pytest test/

run: 
	python main.py 


up:
	docker compose up -d 

down:
	docker compose down 


What is the purpose of declaring .PHONY: at the top of your Makefile, and what happens if you forget to use it when a folder named test exists in your directory?

baceslly the PHONY is to highligh the commands make them vesibele to makefile  if test exists in dir but not in PHONY it wont run it 


Why do we put an @ symbol before a command in a Makefile target (e.g., @echo "Starting...")?

this is to print the messeges for the execution for commands and to print the command list like
help: 
	@echo "run = this runs the project"

	
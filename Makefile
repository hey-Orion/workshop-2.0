.PHONY: install test run clean up down logs


install:
	pip install -r requirements.txt

test:
	pytest tests/

run: 
	python src/main.py 

clean:
	rm -rf data/


up:
	docker compose up -d --build

down: 
	docker compose down -v 

logs:
	docker compose logs -f dataops_worker

	
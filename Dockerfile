FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt . 
RUN pip install --no-catch-dir -r requirements.txt

COPY src/ ./src

ENV PYTHONUNBUFFERD=1

CMD ["python", "src/pipeline.py"]



FROM python:3.11-slim

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \ curl \ && rm -rf /var/lib/apt/lists/*

COPY requirements.txt . 

RUN pip install --no-catch-dir -r requirements.txt

COPY script/ . 

ENTRYPOINT [ "python" ]
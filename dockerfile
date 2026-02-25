FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY script/ ./script/
COPY data/ ./data/

CMD ["python", "script/migration.py"]
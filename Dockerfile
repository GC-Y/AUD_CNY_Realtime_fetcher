FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p templates log_history

ENV PORT=8080

CMD gunicorn --bind 0.0.0.0:$PORT app:app
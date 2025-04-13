FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install channels daphne channels_redis
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
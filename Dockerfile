FROM python:3.11.5-slim

WORKDIR /app

# Установка зависимостей для psycopg2
#RUN apt-get update && apt-get install -y \
#    gcc \
#    python3-dev \
#    libpq-dev

COPY /requirements.txt /

RUN pip install -r /requirements.txt --no-cache-dir

COPY . .

#CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN mkdir static
RUN python manage.py collectstatic --noinput
RUN python3 manage.py makemigrations EventAPI
RUN python3 manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "makemigrations", "EventAPI"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

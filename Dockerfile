FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt requirements.txt
COPY setup.py setup.py
RUN pip install -r requirements.txt
COPY . .
#CMD gunicorn portal.wsgi --bind 0.0.0.0:8000

from python:3.10

LABEL Author="Abdullah Amin Firdaus"

ENV PYTHONBUFFERED 1

COPY chatservice/ /

WORKDIR /chatservice

RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate

from python:3.10

LABEL Author="Abdullah Amin Firdaus"

ENV PYTHONBUFFERED 1

RUN mkdir /chatservice

WORKDIR /chatservice

COPY chatservice/ /chatservice/

RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate

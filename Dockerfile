# Main docker image
FROM python:3.8

# Enviroment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /job_finder
WORKDIR /job_finder

VOLUME /db

# Installing OS dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
libsqlite3-dev
RUN pip install -U pip setuptools
COPY requirements.txt /job_finder
RUN pip install -r /job_finder/requirements.txt
ADD . /job_finder/

# Django service port
EXPOSE 8000

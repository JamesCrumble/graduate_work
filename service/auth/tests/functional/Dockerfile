FROM python:3.11

RUN apt update
WORKDIR /opt/app/

COPY requirements.txt requirements.txt
RUN  pip install -r requirements.txt --no-cache-dir

COPY . .

RUN useradd -ms /bin/bash  sprint_test
USER sprint_test

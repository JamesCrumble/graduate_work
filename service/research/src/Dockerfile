FROM python:3.10
ENV PYTHONUNBUFFERED 1

WORKDIR /opt/app

COPY . .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt  --no-cache-dir

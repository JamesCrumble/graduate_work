FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y gettext netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app/

COPY . .

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt  --no-cache-dir


RUN chmod +x /opt/app/entrypoint.sh

RUN useradd -ms /bin/bash  sprint

USER sprint

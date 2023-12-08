FROM python:3.11

RUN apt update && apt install -y netcat-traditional && pip install --upgrade pip

WORKDIR /opt/app/

COPY requirements.txt requirements.txt

RUN  pip install -r requirements.txt  --no-cache-dir

EXPOSE 4777

COPY . .

RUN chmod +x /opt/app/entrypoint.sh

RUN useradd -ms /bin/bash  sprint

USER sprint

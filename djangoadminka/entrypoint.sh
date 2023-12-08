#!/bin/sh

if [ "$POSTGRES_DB" = "movies_database" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py collectstatic --noinput
python manage.py compilemessages -l en -l ru
python manage.py migrate
python manage.py createsuperuser --noinput || true

uwsgi --ini uwsgi.ini

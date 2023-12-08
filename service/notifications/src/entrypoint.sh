>&2 echo "FROM Notification Container: waiting connection $RABBITMQ_HOST:$RABBITMQ_PORT !!!"

while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
      sleep 1
done

>&2 echo "FROM Notification Container: connection established $RABBITMQ_HOST:$RABBITMQ_PORT !!!"


sgi=$1;
entrypoint="python3 run.py";

if [[ $sgi == "prod" ]]; then
      entrypoint="gunicorn -k uvicorn.workers.UvicornWorker app:app";
fi

$entrypoint &
python3 -u consume_worker.py

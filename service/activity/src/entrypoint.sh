>&2 echo "FROM SEARCH Container ES $MONGODB_HOST:$MONGODB_PORT WAITING!!!"

while ! nc -z $MONGODB_HOST $MONGODB_PORT; do
      sleep 1
done

>&2 echo "FROM SEARCH Container ES $MONGODB_HOST:$MONGODB_PORT STARTED!!!"

sgi=$1;
entrypoint="python3 run.py";

if [[ $sgi == "prod" ]]; then
      entrypoint="gunicorn -k uvicorn.workers.UvicornWorker app:app";
fi

$entrypoint

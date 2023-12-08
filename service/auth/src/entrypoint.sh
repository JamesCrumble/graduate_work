sgi=$1;
entrypoint="python3 run.py";

if [[ $sgi == "prod" ]]; then
      entrypoint="gunicorn -k uvicorn.workers.UvicornWorker app:app";
fi

python3 -m alembic upgrade head;
$entrypoint

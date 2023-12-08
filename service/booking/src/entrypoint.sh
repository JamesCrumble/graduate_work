sgi=$1;
entrypoint="python3 run.py";

if [[ $sgi == "prod" ]]; then
      entrypoint="gunicorn -k uvicorn.workers.UvicornWorker app:app";
fi

$entrypoint &
python3 -u scheduler.py

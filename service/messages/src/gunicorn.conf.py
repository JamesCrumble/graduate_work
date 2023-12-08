from settings import settings

bind = 'unix:/tmp/gunicorn.sock'
workers = settings.workers
reload = settings.enable_autoreload
worker_class = 'gevent'

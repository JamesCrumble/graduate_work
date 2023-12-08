import uvicorn
from settings import settings
from uvicorn.config import LOGGING_CONFIG

if __name__ == '__main__':
    try:
        LOGGING_CONFIG['formatters']['default']['datefmt'] = '%Y-%m-%d %H:%M:%S'
        LOGGING_CONFIG['formatters']['default']['fmt'] = '(%(asctime)s) %(levelprefix)s %(message)s'
        LOGGING_CONFIG['formatters']['access']['datefmt'] = '%Y-%m-%d %H:%M:%S'
        fmt = '(%(asctime)s) %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
        LOGGING_CONFIG['formatters']['access']['fmt'] = fmt
        # noqa
    except Exception:
        pass

    uvicorn.run('app:app', host=settings.HOST, port=settings.PORT, reload=settings.enable_autoreload, workers=settings.workers)

import logging

from settings import settings

logging.basicConfig(
    format='%(asctime)s, %(msecs)d %(name)s %(levelname)s: %(message)s',
    datefmt='%H:%M:%S',
    level=settings.logging_level,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('uvicorn')
es_logger = logging.getLogger('es_logger')
redis_logger = logging.getLogger('redis_logger')

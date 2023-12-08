import os
import sys

import backoff
from redis import Redis
from redis import exceptions as rdexc

from .logger import logger

redis_host: str = str(os.getenv('REDIS_HOST', '127.0.0.1'))
redis_port: int = int(os.getenv('REDIS_PORT', 6379))


@backoff.on_exception(
    backoff.expo,
    (rdexc.ConnectionError, ),
    max_tries=10,
    max_time=10,
)
def wait_service(redis_client):
    if not redis_client.ping():
        raise rdexc.ConnectionError('ERROR STARTING REDIS')
    return True


if __name__ == '__main__':
    logger.debug('WATING FOR REDIS SUCCESSFULLY STARTING')
    redis = Redis(host=redis_host, port=redis_port)
    try:
        wait_service(redis)
    except BaseException as exc:
        logger.debug(f'ERROR STARTING REDIS => "{exc}" (Cannot ping destination mostly)')
        sys.exit(1)
    logger.debug('REDIS SUCCESSFULLY STARTED')

import os
import sys

import backoff
import requests

from .logger import logger

service_host: str = str(os.getenv('SERVICE_HOST', '127.0.0.1'))
service_port: int = int(os.getenv('SERVICE_PORT', 4600))


@backoff.on_exception(
    backoff.expo,
    (ConnectionError, ),
    max_tries=10,
    max_time=10,
)
def wait_service():
    try:
        response = requests.get(
            f'http://{service_host}:{service_port}/activity/api/ping',
            timeout=5, headers={'X-Request-Id': 'test'}
        )
        if response.status_code == 200:
            return True
        else:
            logger.debug(f'Wrong response code => {response.status_code} {response.text}')
            raise ConnectionError()
    except:  # noqa
        raise ConnectionError('Error starting activity service')


if __name__ == '__main__':
    logger.debug('WATING FOR API SERVICE SUCCESSFULLY STARTING')
    try:
        wait_service()
    except Exception as e:
        logger.error(e)
        logger.debug(f'http://{service_host}:{service_port}/activity/api/ping')
        logger.debug('ERROR STARTING API')
        sys.exit(1)
    logger.debug('API SERVICE SUCCESSFULLY STARTED')

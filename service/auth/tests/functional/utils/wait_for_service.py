import os
import sys

import backoff
import requests

from .logger import logger

service_host: str = str(os.getenv('SERVICE_HOST', '127.0.0.1'))
service_port: int = int(os.getenv('SERVICE_PORT', 4000))


@backoff.on_exception(
    backoff.expo,
    (ConnectionError, ),
    max_tries=10,
    max_time=10,
)
def wait_service():
    try:
        response = requests.get(f'http://{service_host}:{service_port}/api/ping', timeout=1)
        if response.status_code == 200:
            return True
        else:
            raise ConnectionError(f'Wrong response code => {response.status_code} {response.text}')
    except BaseException as exc:
        raise ConnectionError(exc)


if __name__ == '__main__':
    logger.debug('WATING FOR AUTH SERVICE SUCCESSFULLY STARTING')
    try:
        wait_service()
    except Exception as e:
        logger.debug(f'ERROR STARTING AUTH SERVICE => "{e}"')
        sys.exit(1)
    logger.debug('AUTH SERVICE SUCCESSFULLY STARTED')

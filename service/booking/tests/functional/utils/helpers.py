from calendar import timegm
from datetime import datetime, timedelta, timezone

import jwt

from ..settings import test_settings
from ..testdata.auth_test_user import PRIVATE_KEY


def build_endpoint_path(endpoint: str) -> str:
    endpoint = endpoint.removeprefix('/').removesuffix('/')
    return f'http://{test_settings.service_host}:{test_settings.service_port}/booking/api/v1/{endpoint}'  # noqa


def build_ws_endpoint_path(endpoint: str) -> str:
    endpoint = endpoint.removeprefix('/').removesuffix('/')
    return f'ws://{test_settings.service_host}:{test_settings.service_port}/messages/api/v1/{endpoint}'  # noqa


def get_access_token(uuid: str):
    token: str = jwt.encode({
        'user_id': uuid,
        'exp': timegm((datetime.now(timezone.utc) + timedelta(minutes=30)).utctimetuple()),
        'iat': timegm(datetime.now(timezone.utc).utctimetuple())
    }, PRIVATE_KEY, algorithm='RS256')
    return token

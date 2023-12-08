from tests.functional.settings import test_settings


def build_endpoint_path(endpoint: str) -> str:
    endpoint = endpoint.removeprefix('/').removesuffix('/')
    return f'http://{test_settings.service_host}:{test_settings.service_port}/notifications/api/v1/{endpoint}'  # noqa

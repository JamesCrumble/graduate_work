from redis import Redis

from ..settings import test_settings


def delete_all_data():
    redis = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    redis.flushall()


if __name__ == '__main__':
    delete_all_data()

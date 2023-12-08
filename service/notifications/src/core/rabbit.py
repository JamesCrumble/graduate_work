from aio_pika.abc import (
    AbstractRobustChannel,
    AbstractRobustConnection,
    AbstractRobustQueue,
)

rabbit_connection: AbstractRobustConnection = None
rabbit_channel: AbstractRobustChannel = None
rabbit_queue_email: AbstractRobustQueue = None
rabbit_queue_push: AbstractRobustQueue = None


def get_rabbit_connection() -> AbstractRobustConnection:
    return rabbit_connection


def get_rabbit_channel() -> AbstractRobustChannel:
    return rabbit_channel


def get_rabbit_queue_email() -> AbstractRobustQueue:
    return rabbit_queue_email


def get_rabbit_queue_push() -> AbstractRobustQueue:
    return rabbit_queue_push

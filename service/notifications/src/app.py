import logging
import time
import uuid
from contextlib import asynccontextmanager

import aio_pika
import backoff
import fastapi
import sentry_sdk
from aio_pika.exceptions import AMQPConnectionError
from api import router as notifications_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core import rabbit
from core.rabbit import get_rabbit_connection
from fastapi import Request, Response, status
from fastapi.responses import ORJSONResponse
from schedule_jobs import jobs_registry
from sentry_sdk.integrations.fastapi import FastApiIntegration
from settings import settings
from starlette.middleware.cors import CORSMiddleware

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    integrations=[FastApiIntegration()]
)


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    @backoff.on_exception(backoff.expo,  AMQPConnectionError)
    async def _connect():
        conn_str = 'amqp://{rabbitmq_default_user}:{rabbitmq_default_pass}@{rabbitmq_host}:{rabbitmq_port}/'.format(
            rabbitmq_default_user=settings.RABBITMQ_DEFAULT_USER,
            rabbitmq_default_pass=settings.RABBITMQ_DEFAULT_PASS,
            rabbitmq_host=settings.RABBITMQ_HOST,
            rabbitmq_port=settings.RABBITMQ_PORT
        )
        return await aio_pika.connect_robust(conn_str)

    rabbit.rabbit_connection = await _connect()
    rabbit.rabbit_channel = await rabbit.rabbit_connection.channel()

    rabbit.rabbit_queue_email = await rabbit.rabbit_channel.declare_queue(settings.rabbit_queue_email_name,
                                                                          durable=True)
    rabbit.rabbit_queue_push = await rabbit.rabbit_channel.declare_queue(settings.rabbit_queue_web_push_name,
                                                                         durable=True)

    jobs_scheduler = AsyncIOScheduler()
    await jobs_registry(jobs_scheduler)
    jobs_scheduler.start()
    logging.info(f'Start jobs scheduler: {jobs_scheduler.get_jobs()}')

    yield

    await get_rabbit_connection().close()
    jobs_scheduler.shutdown()


app = fastapi.FastAPI(
    title=settings.project_name,
    docs_url='/notifications/api/openapi',
    openapi_url='/notifications/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    version=settings.version,
    description=settings.description
)

app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_credentials=True, allow_headers=['*']
)


@app.middleware('http')
async def request_id_required_middleware(request: Request, call_next):
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        if not settings.ignore_request_id:
            return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'detail': 'X-Request-Id is required'})

        request_id = str(uuid.uuid4())

    st = time.monotonic()
    response: Response = await call_next(request)
    response.headers['X-Process-Time'] = str(time.monotonic() - st)

    return response


app.include_router(notifications_router)

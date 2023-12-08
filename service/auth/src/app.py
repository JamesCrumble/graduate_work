import time
from contextlib import asynccontextmanager

import fastapi
import sentry_sdk
from api import auth_router
from core import redis
from core.throttling import ThrottlingMiddleware
from fastapi import Request, status
from fastapi.responses import ORJSONResponse
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from redis.asyncio import Redis
from sentry_sdk.integrations.fastapi import FastApiIntegration
from settings import settings
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

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


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider(resource=Resource.create({SERVICE_NAME: 'auth-service'})))

    jaeger_exporter = JaegerExporter(
        # configure agent
        agent_host_name=settings.jaeger_host,
        agent_port=settings.jaeger_port,

    )

    span_processor = BatchSpanProcessor(jaeger_exporter)

    # add to the tracer
    trace.get_tracer_provider().add_span_processor(span_processor)


if settings.enable_tracer:
    configure_tracer()


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    redis.redis = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
    )
    yield
    await redis.redis.close()


app = fastapi.FastAPI(
    title=settings.project_name,
    docs_url='/auth/api/openapi',
    openapi_url='/auth/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    version=settings.version,
    description=settings.description
)


@app.middleware('http')
async def request_id_required_middleware(request: Request, call_next):
    request_id = request.headers.get('X-Request-Id')
    if not request_id and request.url.path != '/auth/api/openapi' and request.url.path != '/auth/api/openapi.json':
        if not settings.ignore_request_id:
            return ORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={'detail': 'X-Request-Id is required'})

    st = time.monotonic()
    response = await call_next(request)
    response.headers['X-Process-Time'] = str(time.monotonic() - st)

    if settings.enable_tracer:
        trace_id = trace.get_current_span().get_span_context().trace_id
        response.headers['X-Trace-Id'] = format(trace_id, 'x')
    return response

app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_credentials=True, allow_headers=['*']
)
app.add_middleware(
    ThrottlingMiddleware,
    limit=settings.throttling_limit,
    window=settings.throttling_window,
    redis=Redis(
        host=settings.redis_host,
        port=settings.redis_port,
    )
)

app.add_middleware(SessionMiddleware, secret_key='maihoonjiyan')

app.include_router(auth_router)

if settings.enable_tracer:
    FastAPIInstrumentor.instrument_app(app)

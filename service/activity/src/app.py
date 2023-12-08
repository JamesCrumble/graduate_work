import time
import uuid
from contextlib import asynccontextmanager

import fastapi
import sentry_sdk
from api import router as movies_router
from core import mongodb
from core.mongodb import MongoDBConnectionString
from fastapi import Request, Response, status
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
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
    connection_string = str(MongoDBConnectionString(
        host=settings.mongodb_host,
        port=settings.mongodb_port,
        username=settings.mongodb_username,
        password=settings.mongodb_password,
        database=settings.mongodb_database,
    ))
    mongodb.mongo_db = AsyncIOMotorClient(connection_string)

    yield


app = fastapi.FastAPI(
    title=settings.project_name,
    docs_url='/activity/api/openapi',
    openapi_url='/activity/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    version=settings.version,
    description=settings.description
)

app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_credentials=True, allow_headers=['*']
)
app.include_router(movies_router)


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

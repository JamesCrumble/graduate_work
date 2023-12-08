from fastapi import status
from redis.asyncio import Redis
from starlette.datastructures import Headers
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from .logger import logger


class ThrottlingResponse(JSONResponse):
    def __init__(self):
        content = {'detail': 'Too Many Requests'}
        status_code = status.HTTP_429_TOO_MANY_REQUESTS
        super().__init__(status_code=status_code, content=content)


class ThrottlingMiddleware:
    # default value for middleware, values set in app declaration
    def __init__(
        self,
        app: ASGIApp,
        limit: int = 100,
        window: int = 60,
        token_header: str = 'Authorization',
        redis: Redis | None = None,
    ) -> None:
        self.app = app
        self.token_header = token_header
        self.limit = limit
        self.window = window
        self.redis = redis

    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        headers = Headers(scope=scope)
        client_ip = None

        if scope and 'client' in scope and scope['client']:
            client_ip = scope['client'][0]

        client_ip = headers.get(
            'x-forwarded-for', client_ip
        )
        # Throttle by IP
        logger.debug(f'throttling ip: {client_ip}')
        if client_ip and await self.has_exceeded_rate_limit(client_ip):
            response = ThrottlingResponse()
            await response(scope, receive, send)
            return

        token = headers.get(self.token_header)
        # Throttle by Token
        if token and await self.has_exceeded_rate_limit(token):
            response = ThrottlingResponse()
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)
        return

    async def has_exceeded_rate_limit(self, identifier: str) -> bool:
        current_count = await self.redis.get(identifier)

        if current_count is None:
            # This is the first request with this identifier within the window
            await self.redis.set(identifier, 1, ex=self.window)  # Start a new window
            return False

        if int(current_count) < self.limit:
            # Increase the request count
            await self.redis.incr(identifier)
            return False

        return True

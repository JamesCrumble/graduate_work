from calendar import timegm
from datetime import datetime, timedelta, timezone
from json import dumps
from typing import Any

import jwt
from db.storage import RedisStorage
from pydantic import BaseModel
from settings import settings

PRIVATE_SECRET_KEY = settings.private_secret_key.replace('\\n', '\n').encode('utf8')
PUBLIC_SECRET_KEY = settings.public_secret_key.replace('\\n', '\n').encode('utf8')
ALGORITHM = 'RS256'
ACCESS_EXPIRATION_TIME = timedelta(minutes=settings.access_token_expire_minutes)
REFRESH_EXPIRATION_TIME = timedelta(minutes=settings.refresh_token_expire_minutes)


class UserPayload(BaseModel):
    user_id: str
    username: str | None
    groups: list[str] | None
    browser_fingerprint: str | None
    grant_type: str | None
    is_super_user: bool | None = None


class TokenPayload(UserPayload):
    exp: int
    iat: int


class JWTToken:
    access_token: str
    created: datetime
    payload: UserPayload

    def __init__(self, payload: UserPayload):
        self.created = self.get_now()
        self.payload = payload
        self.access_token = self.create_jwt_token(
            payload.dict(exclude_none=True),
            self.created,
            self.access_expiration(self.created)
        )

    @staticmethod
    def create_jwt_token(payload: dict, created: datetime, expiration: datetime) -> str:
        payload.update({'exp': timegm(expiration.utctimetuple())})
        payload.update({'iat': timegm(created.utctimetuple())})
        token: str = jwt.encode(payload, PRIVATE_SECRET_KEY, algorithm=ALGORITHM)
        return token

    @staticmethod
    def verify_jwt_token(token: str) -> Any | None:
        try:
            payload: dict = jwt.decode(token, PUBLIC_SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.PyJWTError:
            return None

        return payload

    @staticmethod
    def get_jwt_token_payload(token: str) -> TokenPayload | None:
        payload = JWTToken.verify_jwt_token(token)
        if payload is None:
            return None

        return TokenPayload(**payload)

    @staticmethod
    def access_expiration(created: datetime) -> datetime:
        return created + ACCESS_EXPIRATION_TIME

    @staticmethod
    def get_now():
        return datetime.now(timezone.utc)

    @staticmethod
    def token_expired(payload: TokenPayload):
        if payload.exp < timegm(JWTToken.get_now().utctimetuple()):
            return True
        return False

    @staticmethod
    async def token_set_disable(redis_storage: RedisStorage, token: str, token_payload: TokenPayload) -> None:
        if not JWTToken.token_expired(token_payload):
            access_token_delta = token_payload.exp - timegm(JWTToken.get_now().utctimetuple())
            await redis_storage.save_to_cache(
                token,
                token_payload.dict(),
                access_token_delta
            )

    @staticmethod
    async def token_disabled(redis_storage: RedisStorage, token: str) -> bool:
        if await redis_storage.get_from_cache(token) is not None:
            return True

        return False

    def to_dict(self) -> dict:
        return {'access_token': self.access_token}

    @property
    def to_json(self) -> str:
        return dumps(self.to_dict())


class JWTTokenPair(JWTToken):
    refresh_token: str

    def __init__(self, payload: UserPayload):
        super().__init__(payload)
        payload.grant_type = 'refresh'
        self.refresh_token = self.create_jwt_token(
            payload.dict(exclude_none=True),
            self.created,
            self.refresh_expiration(self.created)
        )

    @staticmethod
    def refresh_expiration(created: datetime) -> datetime:
        return created + REFRESH_EXPIRATION_TIME

    @staticmethod
    def verify_refresh_token(token: str):
        payload = JWTToken.verify_jwt_token(token)
        # token refresh token
        if payload and payload.get('grant_type') == 'refresh':
            # token redis redis
            return payload
        return None

    def to_dict(self) -> dict:
        tokens = super().to_dict()
        tokens.update({'refresh_token': self.refresh_token})
        return tokens


class JWTTokenPairRaw(BaseModel):
    access_token: str | None
    refresh_token: str | None


def _format_timetuple_and_zone(timetuple, zone):
    return '%s, %02d %s %04d %02d:%02d:%02d %s' % (
        ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][timetuple[6]],
        timetuple[2],
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][timetuple[1] - 1],
        timetuple[0], timetuple[3], timetuple[4], timetuple[5],
        zone)


def format_datetime(dt, usegmt=False):
    now = dt.timetuple()
    if usegmt:
        if dt.tzinfo is None or dt.tzinfo != timezone.utc:
            raise ValueError('usegmt option requires a UTC datetime')
        zone = 'GMT'
    elif dt.tzinfo is None:
        zone = '-0000'
    else:
        zone = dt.strftime('%z')
    return _format_timetuple_and_zone(now, zone)

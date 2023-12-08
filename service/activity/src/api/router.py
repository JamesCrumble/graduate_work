from fastapi import APIRouter

from .v1 import router as v1_router

router = APIRouter(prefix='/activity/api')
router.include_router(v1_router, prefix='/v1')

router.add_api_route(
    path='/ping',
    endpoint=lambda: 'pong',
    methods=['GET'],
    tags=['other']
)


def error():
    return int('ewq')


router.add_api_route(
    path='/error',
    endpoint=error,
    methods=['GET'],
    tags=['other']
)

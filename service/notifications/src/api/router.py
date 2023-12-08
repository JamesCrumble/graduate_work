from fastapi import APIRouter

from .v1 import router as v1_router

router = APIRouter(prefix='/notifications/api')
router.include_router(v1_router, prefix='/v1')

router.add_api_route(
    path='/ping',
    endpoint=lambda: 'pong',
    methods=['GET'],
    tags=['other']
)

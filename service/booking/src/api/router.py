from fastapi import APIRouter

from .v1.router import router as v1_router

router = APIRouter(prefix='/api')
router.include_router(v1_router)

router.add_api_route(
    path='/ping',
    endpoint=lambda: 'pong',
    methods=['GET'],
    tags=['other']
)

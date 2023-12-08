from fastapi import APIRouter, Depends, Header

from .v1 import router as v1_router


def custom_headers(x_request_id: str = Header()):
    return 'X_Request_Id'


router = APIRouter(prefix='/auth/api', dependencies=[Depends(custom_headers)])

router.include_router(v1_router, prefix='/v1')

router.add_api_route(
    path='/ping',
    endpoint=lambda: 'pong',
    methods=['GET'],
    tags=['other']
)

from core.auth_token import token_payload_dependency
from fastapi import APIRouter, Depends

from .flim_events import router as film_events_router
from .tickets import router as tickets_router

router = APIRouter(prefix='/v1')
router.include_router(film_events_router, dependencies=[Depends(token_payload_dependency)])
router.include_router(tickets_router, dependencies=[Depends(token_payload_dependency)])

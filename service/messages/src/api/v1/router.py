from fastapi import APIRouter

from .sms.router import router as sms_router

router = APIRouter(prefix='/v1')
router.include_router(sms_router)

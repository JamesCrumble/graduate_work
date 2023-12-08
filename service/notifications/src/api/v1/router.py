from fastapi import APIRouter

from .queue.router import router as queue_router

router = APIRouter()
router.include_router(queue_router, prefix='/queue')

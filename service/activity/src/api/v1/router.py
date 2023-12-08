from fastapi import APIRouter

from .bookmarks.router import router as bookmarks_router
from .likes.router import router as likes_router
from .reviews.router import router as reviews_router

router = APIRouter()
router.include_router(likes_router, prefix='/likes')
router.include_router(reviews_router, prefix='/reviews')
router.include_router(bookmarks_router, prefix='/bookmarks')

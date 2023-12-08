from core.mongodb import get_client
from db.tables import MoviesUserLike
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.database import Database

from ..common.controller import BaseController


class LikesController(BaseController):
    collection = 'movies_user_like'
    model_class = MoviesUserLike


async def get_likes_service(
    engine: Database | AsyncIOMotorDatabase = Depends(get_client)
):
    return LikesController(engine)

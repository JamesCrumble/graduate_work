from core.mongodb import get_client
from db.tables import MoviesUserBookmark
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.database import Database

from ..common.controller import BaseController


class BookmarksController(BaseController):
    collection = 'movies_user_bookmark'
    model_class = MoviesUserBookmark


async def get_bookmark_service(
    engine: Database | AsyncIOMotorDatabase = Depends(get_client)
):
    return BookmarksController(engine)

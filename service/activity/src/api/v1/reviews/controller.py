from core.mongodb import get_client
from db.tables import MoviesReview
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.database import Database

from ..common.controller import BaseController


class ReviewsController(BaseController):
    collection = 'movies_user_review'
    model_class = MoviesReview


async def get_reviews_service(
    engine: Database | AsyncIOMotorDatabase = Depends(get_client)
):
    return ReviewsController(engine)

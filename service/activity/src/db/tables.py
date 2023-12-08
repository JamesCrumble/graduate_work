from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, validator


class MoviesUserLike(BaseModel):
    id: UUID | None
    user_id: UUID
    movie_id: UUID
    like: int
    created: datetime | None

    @validator('user_id', 'movie_id', 'id')
    def validate_uuids(cls, value):
        if value:
            return str(value)
        return value


class MoviesReview(BaseModel):
    id: UUID | None
    description: str
    text: str
    created: datetime | None
    updated: datetime
    author_id: UUID
    movie_id: UUID

    @validator('author_id', 'movie_id', 'id')
    def validate_uuids(cls, value):
        if value:
            return str(value)
        return value


class MoviesUserBookmark(BaseModel):
    id: UUID | None
    user_id: UUID
    movie_id: UUID
    created: datetime | None

    @validator('user_id', 'movie_id', 'id')
    def validate_uuids(cls, value):
        if value:
            return str(value)
        return value

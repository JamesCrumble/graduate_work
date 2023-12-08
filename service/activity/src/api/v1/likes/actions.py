from uuid import UUID

from core.authorization import get_user_from_access_token
from core.users import BaseUserAuth
from db.tables import MoviesUserLike
from fastapi import Depends, Path, Query

from ..common.http_exceptions import NotAuthenticated
from ..common.params import CommonParams
from .controller import LikesController, get_likes_service


async def list_movie_user_like(
    likes_service: LikesController = Depends(get_likes_service),
    movie_id: UUID | None = Query(default=None),
    params: CommonParams = Depends(CommonParams)
):
    filter_params = {}
    if movie_id:
        filter_params['movie_id'] = str(movie_id)
    find_obj = await likes_service.list(params, filter_params)
    return find_obj


async def create_movie_user_like(
    body: MoviesUserLike,
    likes_service: LikesController = Depends(get_likes_service),
    user_auth: BaseUserAuth = Depends(get_user_from_access_token),
):
    if not user_auth.is_authenticated:
        raise NotAuthenticated
    created_obj = await likes_service.create(body)
    return created_obj


async def get_movie_user_like(
    uuid: UUID = Path(..., description='get movie like by id'),
    likes_service: LikesController = Depends(get_likes_service)
):
    find_obj = await likes_service.read(uuid)
    return find_obj


async def update_movie_user_like(
    body: MoviesUserLike,
    uuid: UUID = Path(..., description='update movie like by id'),
    likes_service: LikesController = Depends(get_likes_service),
    user_auth: BaseUserAuth = Depends(get_user_from_access_token),
):
    if not user_auth.is_authenticated:
        raise NotAuthenticated
    find_obj = await likes_service.update(uuid, body)
    return find_obj


async def delete_movie_user_like(
    uuid: UUID = Path(..., description='delete movie like by id'),
    likes_service: LikesController = Depends(get_likes_service),
    user_auth: BaseUserAuth = Depends(get_user_from_access_token),
):
    if not user_auth.is_authenticated:
        raise NotAuthenticated
    find_obj = await likes_service.delete(uuid)
    return find_obj

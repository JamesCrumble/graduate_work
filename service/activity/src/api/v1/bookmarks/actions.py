from uuid import UUID

from core.authorization import get_user_from_access_token
from core.users import BaseUserAuth
from db.tables import MoviesUserBookmark
from fastapi import Depends, Path, Query

from ..common.http_exceptions import NotAuthenticated
from ..common.params import CommonParams
from .controller import BookmarksController, get_bookmark_service


async def list_movie_user_bookmark(
    bookmark_service: BookmarksController = Depends(get_bookmark_service),
    user_id: UUID | None = Query(default=None),
    params: CommonParams = Depends(CommonParams)
):
    filter_params = {}
    if user_id:
        filter_params['user_id'] = str(user_id)
    find_obj = await bookmark_service.list(params, filter_params)
    return find_obj


async def create_movie_user_bookmark(
    body: MoviesUserBookmark,
    bookmark_service: BookmarksController = Depends(get_bookmark_service),
    user_auth: BaseUserAuth = Depends(get_user_from_access_token),
):
    if not user_auth.is_authenticated:
        raise NotAuthenticated
    created_obj = await bookmark_service.create(body)
    return created_obj


async def get_movie_user_bookmark(
    uuid: UUID = Path(..., description='get movie bookmark by id'),
    bookmark_service: BookmarksController = Depends(get_bookmark_service)
):
    find_obj = await bookmark_service.read(uuid)
    return find_obj


async def update_movie_user_bookmark(
    body: MoviesUserBookmark,
    uuid: UUID = Path(..., description='update movie bookmark by id'),
    bookmark_service: BookmarksController = Depends(get_bookmark_service),
    user_auth: BaseUserAuth = Depends(get_user_from_access_token),
):
    if not user_auth.is_authenticated:
        raise NotAuthenticated
    find_obj = await bookmark_service.update(uuid, body)
    return find_obj


async def delete_movie_user_bookmark(
    uuid: UUID = Path(..., description='delete movie bookmark by id'),
    bookmark_service: BookmarksController = Depends(get_bookmark_service),
    user_auth: BaseUserAuth = Depends(get_user_from_access_token),
):
    if not user_auth.is_authenticated:
        raise NotAuthenticated
    find_obj = await bookmark_service.delete(uuid)
    return find_obj

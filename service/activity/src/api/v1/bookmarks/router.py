from db.tables import MoviesUserBookmark
from fastapi import APIRouter, status

from ..common.service import RequestSuccess
from .actions import (
    create_movie_user_bookmark,
    delete_movie_user_bookmark,
    get_movie_user_bookmark,
    list_movie_user_bookmark,
    update_movie_user_bookmark,
)

router = APIRouter(prefix='', tags=['bookmarks'])

router.add_api_route('/', create_movie_user_bookmark, response_model_by_alias=False, methods=['POST'],
                     response_model=MoviesUserBookmark, description='create movie user bookmark',
                     summary='create movie user bookmark')
router.add_api_route('/{uuid}', get_movie_user_bookmark, response_model_by_alias=False, methods=['GET'],
                     response_model=MoviesUserBookmark, description='read movie user bookmark',
                     summary='read movie user bookmark')
router.add_api_route('/{uuid}', update_movie_user_bookmark, response_model_by_alias=False, methods=['PUT'],
                     response_model=MoviesUserBookmark, description='update movie user bookmark',
                     summary='update movie user bookmark')
router.add_api_route('/{uuid}', delete_movie_user_bookmark, response_model_by_alias=False, methods=['DELETE'],
                     response_model=RequestSuccess, description='delete movie user bookmark',
                     summary='delete movie user bookmark',
                     status_code=status.HTTP_200_OK)
router.add_api_route('/', list_movie_user_bookmark, response_model_by_alias=False, methods=['GET'],
                     response_model=list[MoviesUserBookmark], description='list movie user bookmark',
                     summary='list movie user bookmark',
                     status_code=status.HTTP_200_OK)

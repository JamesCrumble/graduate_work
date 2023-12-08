from db.tables import MoviesUserLike
from fastapi import APIRouter, status

from ..common.service import RequestSuccess
from .actions import (
    create_movie_user_like,
    delete_movie_user_like,
    get_movie_user_like,
    list_movie_user_like,
    update_movie_user_like,
)

router = APIRouter(prefix='', tags=['likes'])

router.add_api_route('/', create_movie_user_like, response_model_by_alias=False, methods=['POST'],
                     response_model=MoviesUserLike, description='create movie user like', summary='create movie user like')
router.add_api_route('/{uuid}', get_movie_user_like, response_model_by_alias=False, methods=['GET'],
                     response_model=MoviesUserLike, description='read movie user like', summary='read movie user like')
router.add_api_route('/{uuid}', update_movie_user_like, response_model_by_alias=False, methods=['PUT'],
                     response_model=MoviesUserLike, description='update movie user like', summary='update movie user like')
router.add_api_route('/{uuid}', delete_movie_user_like, response_model_by_alias=False, methods=['DELETE'],
                     response_model=RequestSuccess, description='delete movie user like', summary='delete movie user like',
                     status_code=status.HTTP_200_OK)
router.add_api_route('/', list_movie_user_like, response_model_by_alias=False, methods=['GET'],
                     response_model=list[MoviesUserLike], description='list movie user like', summary='list movie user like',
                     status_code=status.HTTP_200_OK)

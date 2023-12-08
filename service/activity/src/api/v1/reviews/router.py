from db.tables import MoviesReview
from fastapi import APIRouter, status

from ..common.service import RequestSuccess
from .actions import (
    create_movie_user_review,
    delete_movie_user_review,
    get_movie_user_review,
    list_movie_user_review,
    update_movie_user_review,
)

router = APIRouter(prefix='', tags=['reviews'])

router.add_api_route('/', create_movie_user_review, response_model_by_alias=False, methods=['POST'],
                     response_model=MoviesReview, description='create movie user review', summary='create movie user review')
router.add_api_route('/{uuid}', get_movie_user_review, response_model_by_alias=False, methods=['GET'],
                     response_model=MoviesReview, description='read movie user review', summary='read movie user review')
router.add_api_route('/{uuid}', update_movie_user_review, response_model_by_alias=False, methods=['PUT'],
                     response_model=MoviesReview, description='update movie user review', summary='update movie user review')
router.add_api_route('/{uuid}', delete_movie_user_review, response_model_by_alias=False, methods=['DELETE'],
                     response_model=RequestSuccess, description='delete movie user review', summary='delete movie user review',
                     status_code=status.HTTP_200_OK)
router.add_api_route('/', list_movie_user_review, response_model_by_alias=False, methods=['GET'],
                     response_model=list[MoviesReview], description='list movie user review', summary='list movie user review',
                     status_code=status.HTTP_200_OK)

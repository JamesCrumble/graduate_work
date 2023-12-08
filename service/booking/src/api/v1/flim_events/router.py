from http import HTTPStatus

from fastapi import APIRouter

from .actions import (
    create_user_film_event,
    get_user_film_event,
    get_user_film_events,
    update_user_film_event,
)

router = APIRouter()

router.add_api_route('/film_event', get_user_film_events, methods=['GET'])
router.add_api_route('/film_event/{event_id}', get_user_film_event, methods=['GET'])
router.add_api_route('/film_event', create_user_film_event, methods=['POST'], status_code=HTTPStatus.CREATED)
router.add_api_route('/film_event/{event_id}', update_user_film_event, methods=['PUT'])

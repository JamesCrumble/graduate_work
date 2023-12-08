from http import HTTPStatus

from fastapi import APIRouter

from .actions import (
    create_user_ticket,
    get_ticket_list_all,
    get_user_ticket_info,
    get_user_tickets,
    update_user_ticket,
)

router = APIRouter(prefix='/ticket', tags=['tickets'])

router.add_api_route('/', create_user_ticket,  methods=['POST'],
                     description='create user ticket', summary='create a filmevent ticket',
                     status_code=HTTPStatus.CREATED)

router.add_api_route('/', update_user_ticket,  methods=['PUT'],
                     description='update user ticket status', summary='update user ticket status')

router.add_api_route('/{ticket_id}', get_user_ticket_info,  methods=['GET'],
                     description='get information by user ticket', summary='get information by user ticket')

router.add_api_route('/', get_user_tickets,  methods=['GET'],
                     description='get user ticket list', summary='get user ticket list')

router.add_api_route('/_list/', get_ticket_list_all,  methods=['GET'],
                     description='get a list of all tickets', summary='get a list of all tickets')

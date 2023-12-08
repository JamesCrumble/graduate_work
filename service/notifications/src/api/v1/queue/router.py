import http

from auth_token import token_payload_dependency
from fastapi import APIRouter, Depends

from .actions import (
    add_notification_to_queue_by_email,
    add_notification_to_queue_by_email_on_registration,
    add_notification_to_queue_by_web_push,
)

router = APIRouter(dependencies=[Depends(token_payload_dependency)], prefix='', tags=['queue'])


router.add_api_route('/email', add_notification_to_queue_by_email, response_model_by_alias=False, methods=['POST'],
                     status_code=http.HTTPStatus.CREATED, description='append new notification',
                     summary='append notification to queue')

router.add_api_route('/on_registration', add_notification_to_queue_by_email_on_registration,
                     response_model_by_alias=False, methods=['POST'],
                     status_code=http.HTTPStatus.CREATED, description='append notification when user registrate',
                     summary='append notification to queue when user registrate')

router.add_api_route('/web_push', add_notification_to_queue_by_web_push, response_model_by_alias=False,
                     methods=['POST'], status_code=http.HTTPStatus.CREATED,
                     description='append new web push notification',
                     summary='append notification to queue web push notification')

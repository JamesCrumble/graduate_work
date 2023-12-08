from fastapi import APIRouter, status

from .actions import create_role, get_role, get_role_list, remove_role, update_role
from .schemas import ActionStatus, RoleRead

router = APIRouter(prefix='/roles', tags=['Roles'])

router.add_api_route(path='/', endpoint=get_role_list, response_model=list[RoleRead])

router.add_api_route('/{role_id}', get_role, response_model_by_alias=False, response_model=RoleRead)

router.add_api_route('/',  create_role, methods=['post'],
                     response_model_by_alias=False, response_model=None,
                     responses={
                         status.HTTP_200_OK: {'model': RoleRead},
                         status.HTTP_409_CONFLICT: {'model': ActionStatus}
})

router.add_api_route('/',  update_role, methods=['put'], response_model_by_alias=False, response_model=RoleRead)

router.add_api_route('/',  remove_role, methods=['delete'], response_model_by_alias=False, response_model=ActionStatus)

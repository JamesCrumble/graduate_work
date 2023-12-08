from fastapi import APIRouter, status

from ..schemas import ActionStatus, UserRole
from .actions import get_roles_by_user, remove_user_role, set_user_role

router = APIRouter(prefix='/user_role', tags=['User Roles'])

router.add_api_route('/{user_id}', get_roles_by_user,
                     response_model_by_alias=False, response_model=list[UserRole])


router.add_api_route('', set_user_role, methods=['post'],
                     response_model_by_alias=False, response_model=None,
                     responses={
                         status.HTTP_200_OK: {'model': UserRole},
                         status.HTTP_409_CONFLICT: {'model': ActionStatus}
})

router.add_api_route('', remove_user_role, methods=['delete'],
                     response_model_by_alias=False, response_model=ActionStatus)

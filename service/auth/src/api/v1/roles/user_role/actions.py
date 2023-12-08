from fastapi import Depends, Response

from ...common.permissions import PermissionChecker
from ...schemas.user import BaseUserAuth
from .user_role_service import UserRoleService, get_user_role_service


async def get_roles_by_user(
    user_id: str,
    manager: UserRoleService = Depends(get_user_role_service),
    auth_user: BaseUserAuth = Depends(PermissionChecker('role_admin')),
):
    return await manager.get_user_role(user_id=user_id)


async def set_user_role(
    response: Response,
    user_id: str,
    role_id: str,
    manager: UserRoleService = Depends(get_user_role_service),
    auth_user: BaseUserAuth = Depends(PermissionChecker('role_admin')),
):
    return await manager.set_user_role(user_id=user_id, role_id=role_id, response=response)


async def remove_user_role(
    record_id: str,
    manager: UserRoleService = Depends(get_user_role_service),
    auth_user: BaseUserAuth = Depends(PermissionChecker('role_admin')),
):
    return await manager.remove_user_role(record_id=record_id)

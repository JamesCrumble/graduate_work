from uuid import UUID

from fastapi import Depends, Response

from ..common.permissions import PermissionChecker
from ..schemas.user import BaseUserAuth
from .role_service import RoleService, get_role_service
from .schemas import RoleCreate, RoleUpdate


async def get_role_list(
    manager: RoleService = Depends(get_role_service),
    auth_user: BaseUserAuth = Depends(PermissionChecker('role_admin')),
):
    return await manager.get_list()


async def get_role(
    role_id: UUID,
    manager: RoleService = Depends(get_role_service),
    auth_user: BaseUserAuth = Depends(PermissionChecker('role_admin')),
):
    return await manager.get_item(role_id)


async def create_role(
    response: Response,
    role: RoleCreate,
    manager: RoleService = Depends(get_role_service),
    auth_user: BaseUserAuth = Depends(PermissionChecker('role_admin')),
):
    return await manager.create(role, response)


async def update_role(
    role: RoleUpdate,
    manager: RoleService = Depends(get_role_service),
    auth_user: BaseUserAuth = Depends(PermissionChecker('role_admin')),
):
    return await manager.update(role)


async def remove_role(
    role_id: UUID,
    manager: RoleService = Depends(get_role_service),
    auth_user: BaseUserAuth = Depends(PermissionChecker('role_admin')),
):
    return await manager.remove(role_id)

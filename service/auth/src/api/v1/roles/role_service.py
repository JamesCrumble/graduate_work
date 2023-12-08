from uuid import UUID

from api.v1.common.base_auth_service import BaseService
from api.v1.roles.role_control import RoleControl
from api.v1.roles.schemas import ActionStatus, RoleCreate, RoleRead, RoleUpdate
from db.postgres import service_session
from db.tables import RolesTable
from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession


class RoleService(BaseService):
    _control: RoleControl

    def __init__(self, session: AsyncSession):
        self._control = RoleControl(session)

    async def _get_role_by_id(self, role_id: str) -> RolesTable:
        role: RolesTable = await self._control.get_record_by_id(role_id, RolesTable)
        if not role:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,

                                detail=f'The user role id={role_id} not found'
                                )
        return role

    async def create(self,
                     role_create: RoleCreate,
                     response: Response) -> RoleRead | ActionStatus:

        if await self._control.is_role_exists(role_create.title):
            return self._error(response, status.HTTP_409_CONFLICT, f'User role "{role_create.title}" already exists')

        role = await self._control.create(role_create.title)

        return RoleRead(**role.dict())

    async def update(self, role_update: RoleUpdate) -> RoleRead | ActionStatus:

        role: RolesTable | None = await self._get_role_by_id(str(role_update.id))
        role = await self._control.update(role, role_update.title)
        return RoleRead(**role.dict())

    async def get_item(self, role_id: UUID) -> RoleRead | ActionStatus:
        role: RolesTable = await self._get_role_by_id(str(role_id))
        return RoleRead(**role.dict())

    async def get_list(self) -> [RolesTable]:
        roles = await self._control.all()
        result = [role.dict() for role in roles]
        return result

    async def remove(self, role_id: UUID) -> ActionStatus:
        role: RolesTable | None = await self._get_role_by_id(str(role_id))
        await self._control.remove(role)
        return ActionStatus(status='success', error_message=f'The user role id={role_id} has been successfully deleted')


async def get_role_service(session: AsyncSession = Depends(service_session)) -> RoleService:
    return RoleService(session)

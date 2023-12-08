from api.v1.common.base_auth_service import BaseService
from api.v1.roles.schemas import ActionStatus, UserRole
from api.v1.roles.user_role.user_role_control import UserRoleControl
from db.postgres import service_session
from db.tables import RolesTable, UserRoleTable, UserTable
from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession


class UserRoleService(BaseService):
    _control: UserRoleControl

    def __init__(self, session: AsyncSession):
        self._control = UserRoleControl(session)

    async def _get_record_by_id(self, record_id: str, model, message) -> RolesTable | UserTable | UserRoleTable:
        record: model = await self._control.get_record_by_id(record_id, model)
        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        return record

    async def _get_role_by_id(self, role_id: str) -> RolesTable:
        return await self._get_record_by_id(role_id, RolesTable, f'User role id=\'{role_id}\' not found')

    async def _get_user_by_id(self, user_id: str) -> UserTable:
        return await self._get_record_by_id(user_id, UserTable, f'User id=\'{user_id}\' not found')

    async def _get_user_role_by_id(self, user_role_id: str) -> UserRoleTable:
        return await self._get_record_by_id(user_role_id, UserRoleTable, f'Record id=\'{user_role_id}\' not found')

    async def set_user_role(self, role_id: str, user_id: str,
                            response: Response) -> UserRole | ActionStatus:

        await self._get_role_by_id(role_id)
        await self._get_user_by_id(user_id)

        if await self._control.is_record_exists(user_id=user_id, role_id=role_id):
            return self._error(response, status.HTTP_409_CONFLICT, 'Record already exists')

        user_role: UserRoleTable = await self._control.create(user_id=user_id, role_id=role_id)
        return UserRole(**user_role.dict())

    async def remove_user_role(self, record_id: str) -> ActionStatus:
        user_role: UserRoleTable = await self._get_user_role_by_id(record_id)
        await self._control.remove(user_role)
        return ActionStatus(status='success', error_message=f'Record id={record_id} has been successfully deleted')

    async def get_user_role(self, user_id: str) -> [UserRole]:

        await self._get_user_by_id(user_id)
        records = await self._control.get_items_by_user_id(user_id)
        return [record.dict() for record in records]

    async def get_user_roles(self, user_id: str) -> list[str]:
        records = await self._control.get_user_roles(user_id)
        return records


async def get_user_role_service(session: AsyncSession = Depends(service_session)) -> UserRoleService:
    return UserRoleService(session)

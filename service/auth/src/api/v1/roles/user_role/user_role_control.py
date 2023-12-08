from db.tables import RolesTable, UserRoleTable
from sqlalchemy import ScalarResult, select

from ..base_role_control import RoleBaseControl


class UserRoleControl(RoleBaseControl):

    async def get_user_role_by_id(self, user_role_id: str) -> UserRoleTable:
        return await self.get_record_by_id(user_role_id, UserRoleTable)

    async def is_record_exists(self, user_id: str, role_id: str) -> UserRoleTable:
        q = select(UserRoleTable).filter((UserRoleTable.user_id == user_id) & (UserRoleTable.role_id == role_id))
        result = await self._session.execute(q)
        return result.scalars().first() is not None

    async def create(self, user_id: str, role_id: str) -> UserRoleTable:
        user_role = UserRoleTable(role_id=role_id, user_id=user_id)
        self._session.add(user_role)
        await self._session.commit()
        await self._session.refresh(user_role)
        return user_role

    async def remove(self, record: UserRoleTable) -> None:
        await self._session.delete(record)
        await self._session.commit()

    async def get_items_by_user_id(self, user_id: str) -> ScalarResult[UserRoleTable]:
        q = select(UserRoleTable).filter(UserRoleTable.user_id == user_id)
        result = await self._session.execute(q)
        return result.scalars()

    async def get_user_roles(self, user_id: str) -> list[str]:
        q = select(RolesTable.title).join(UserRoleTable).filter(UserRoleTable.user_id == user_id)
        result = await self._session.execute(q)
        records = result.scalars().all()
        return records

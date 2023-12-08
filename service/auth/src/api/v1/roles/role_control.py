from api.v1.roles.base_role_control import RoleBaseControl
from db.tables import RolesTable
from sqlalchemy import ScalarResult, select


class RoleControl(RoleBaseControl):

    async def get_role_by_id(self, role_id) -> RolesTable:
        return await self.get_record_by_id(role_id, RolesTable)

    async def is_role_exists(self, title: str) -> RolesTable:
        query = select(RolesTable).where(RolesTable.title == title)
        result = await self._session.execute(query)
        return result.first() is not None

    async def create(self, title) -> RolesTable:
        role = RolesTable(title=title)
        self._session.add(role)
        await self._session.commit()
        await self._session.refresh(role)
        return role

    async def update(self, role: RolesTable, title: str) -> RolesTable:
        role.title = title
        await self._session.commit()
        await self._session.refresh(role)
        return role

    async def remove(self, role: RolesTable) -> RolesTable:
        await self._session.delete(role)
        await self._session.commit()
        return role

    async def all(self) -> ScalarResult[RolesTable]:
        q = select(RolesTable)
        result = await self._session.execute(q)
        return result.scalars()

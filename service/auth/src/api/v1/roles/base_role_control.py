from db.tables import RolesTable, UserRoleTable, UserTable
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class RoleBaseControl:
    __slots__ = '_session', '_model'

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_record_by_id(self, record_id: str, model) -> RolesTable | UserTable | UserRoleTable:
        q = select(model).filter(model.id == record_id)
        result = await self._session.execute(q)
        record: RolesTable | UserTable = result.scalars().first()
        return record

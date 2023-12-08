from db.postgres import service_session
from fastapi import Depends, Query
from models import UserHistoryOperation
from sqlalchemy.ext.asyncio import AsyncSession

from ..common.auth_credentials import get_user_from_access_token
from ..http_exceptions import NotAuthenticated
from ..schemas.user import SimpleUserAuth
from ..user_control import UserControl


async def user_history(
    session: AsyncSession = Depends(service_session),
    auth_user: SimpleUserAuth = Depends(get_user_from_access_token),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    if not auth_user.is_authenticated:
        raise NotAuthenticated

    user_control = UserControl(session)

    return await user_control.get_user_history(
        auth_user.user_payload.user_id,
        [UserHistoryOperation.LOGIN],
        (page - 1) * page_size,
        page_size
    )

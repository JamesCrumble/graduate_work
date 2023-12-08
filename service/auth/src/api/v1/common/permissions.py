from fastapi import Depends

from ..http_exceptions import PermissionDenied
from ..schemas.user import SimpleUserAuth
from .auth_credentials import get_user_from_access_token


class PermissionChecker:

    def __init__(self, permissions: list[str] | str | None):
        if isinstance(permissions, str):
            permissions = [permissions]
        self.permissions = permissions

    async def __call__(self, auth_user: SimpleUserAuth = Depends(get_user_from_access_token)) -> SimpleUserAuth:
        """
                 Generated dependency function
        """
        if not auth_user.is_authenticated:
            raise PermissionDenied

        if auth_user.is_super_user:
            return auth_user
        if not self.permissions:
            return auth_user
        has_permission = False
        for need_permission in self.permissions:
            if need_permission in auth_user.user_payload.groups:
                has_permission = True
        if not has_permission:
            raise PermissionDenied
        return auth_user

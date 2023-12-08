from fastapi import HTTPException, status


class LoginError(HTTPException):
    ...


class UserExists(HTTPException):
    ...


class EmptyField(HTTPException):
    ...


class NotAuthenticated(HTTPException):
    def __init__(self, headers: dict[str, str] | None = None) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, 'Not authenticated', headers)


class ForbiddenRequest(HTTPException):
    def __init__(self, headers: dict[str, str] | None = None) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, 'Forbidden request', headers)


class PermissionDenied(HTTPException):
    def __init__(self, headers: dict[str, str] | None = None) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, 'Permission denied', headers)


class ChangePasswordError(HTTPException):
    ...


class NotFound(HTTPException):
    def __init__(self, headers: dict[str, str] | None = None) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, 'Not found', headers)


class BadRequest(HTTPException):
    def __init__(self, headers: dict[str, str] | None = None) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, 'Bad request', headers)

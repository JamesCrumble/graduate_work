from abc import ABC

from api.v1.roles.schemas import ActionStatus
from fastapi.openapi.models import Response


class BaseService(ABC):

    def __repr__(self) -> str:
        return self.__class__.__name__

    @staticmethod
    def _error(response: Response, error_code: int, error_message: str) -> ActionStatus:
        response.status_code = error_code
        return ActionStatus(status='error', error_message=error_message)

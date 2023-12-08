from collections.abc import Callable
from typing import TypeVar

from fastapi import APIRouter
from pydantic import BaseModel

from .service import CRUDService

T = TypeVar('T', bound=BaseModel)


class BaseRouter(APIRouter):

    def __init__(self, model_cls: BaseModel, service: Callable[..., CRUDService]):
        self.router = APIRouter()
        self.model = model_cls
        self.service = service()
        self.setup_routes()

    def setup_routes(self):
        @self.router.post('/')
        async def create(item: self.model):
            return await self.service.create(item)

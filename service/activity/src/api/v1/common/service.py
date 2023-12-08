from abc import ABC, abstractmethod

from pydantic import BaseModel


class BaseService(ABC):
    table = BaseModel

    def __init__(self, engine):
        self.engine = engine

    def __repr__(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    async def list(self) -> list[dict]:
        ...

    @abstractmethod
    async def read(self, _id: str) -> dict:
        ...

    @abstractmethod
    async def create(self, item):
        ...

    @abstractmethod
    async def delete(self) -> None:
        ...

    @abstractmethod
    async def update(self) -> None:
        ...


class CRUDService(BaseService):
    async def list(self) -> list[dict]:
        ...

    async def read(self, _id: str) -> dict:
        ...

    async def create(self, item):
        ...

    async def delete(self) -> None:
        ...

    async def update(self) -> None:
        ...


class RequestSuccess(BaseModel):
    detail: str

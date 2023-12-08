from collections.abc import Callable
from uuid import UUID

from db.orm import MongoDBNoSqlCollectionORM
from pydantic import BaseModel
from pymongo.errors import PyMongoError

from .http_exceptions import BadRequest, NotFound
from .params import CommonParams
from .service import RequestSuccess


class BaseController:
    model_class: Callable[..., BaseModel]
    collection: str
    orm: MongoDBNoSqlCollectionORM

    def __init__(self, engine):
        if not hasattr(self, 'model_class'):
            raise ValueError(f'{self.__class__.__name__} must set model class')
        if not hasattr(self, 'collection'):
            raise ValueError(f'{self.__class__.__name__} must set mongo db collection')
        self.orm = MongoDBNoSqlCollectionORM(engine)

    def __repr__(self) -> str:
        return self.__class__.__name__

    async def list(self, params: CommonParams, filter_params: dict = None) -> list[BaseModel]:
        objects = await self.orm.find(self.collection, params.page_number, params.page_size, filter_params)
        return objects

    async def read(self, uuid: str | UUID) -> BaseModel:
        object = await self.orm.find_one(self.collection, uuid)
        if not object:
            raise NotFound
        return object

    async def create(self, obj: BaseModel) -> BaseModel:
        try:
            object_model = self.model_class(**obj.dict())
            return_obj = await self.orm.insert_one(self.collection, object_model)
        except PyMongoError:
            raise BadRequest()

        return return_obj

    async def update(self, uuid: str | UUID, obj: BaseModel):
        return await self.orm.update_one(self.collection, uuid, obj)

    async def delete(self, uuid: str | UUID):
        result_obj = await self.orm.delete_one(self.collection, uuid)
        if not result_obj:
            raise NotFound
        return RequestSuccess(detail='success')

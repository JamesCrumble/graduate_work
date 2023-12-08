from typing import Any, Coroutine
from uuid import UUID, uuid4

import backoff
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from pydantic import BaseModel
from pymongo import ReturnDocument
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError
from settings import settings


class MongoDBNoSqlCollectionORM():
    engine: AsyncIOMotorClient
    database: Database | AsyncIOMotorDatabase

    def __init__(self, engine: Database | AsyncIOMotorDatabase):
        self.engine = engine
        self.database = engine.get_database(settings.mongodb_database)

    async def __get_collection(self, collection: str) -> Coroutine[Any, Any, Collection] | AsyncIOMotorCollection:
        return self.database.get_collection(collection)

    @staticmethod
    def __get_object(obj: dict | BaseModel):
        ret_obj = obj
        if isinstance(ret_obj, BaseModel):
            ret_obj = ret_obj.dict()
        if ret_obj['id']:
            ret_obj['_id'] = ret_obj['id']
        if '_id' not in ret_obj:
            ret_obj['_id'] = str(uuid4())
            ret_obj['id'] = ret_obj['_id']
        return ret_obj

    @backoff.on_exception(backoff.expo, (PyMongoError, ), max_tries=20, max_time=120)
    async def insert_one(self, collection: str, obj: dict | BaseModel):
        ins_obj = self.__get_object(obj)
        collection_orm = await self.__get_collection(collection)
        await collection_orm.insert_one(ins_obj)
        return ins_obj

    @backoff.on_exception(backoff.expo, (PyMongoError, ), max_tries=20, max_time=120)
    async def find_one(self, collection: str, _id: UUID):
        collection_orm = await self.__get_collection(collection)
        obj_id = str(_id)
        result_obj = await collection_orm.find_one({'_id': obj_id})
        return result_obj

    @backoff.on_exception(backoff.expo, (PyMongoError, ), max_tries=20, max_time=120)
    async def delete_one(self, collection: str, _id: UUID):
        collection_orm = await self.__get_collection(collection)
        obj_id = str(_id)
        result_obj = await collection_orm.find_one_and_delete({'_id': obj_id})
        return result_obj

    @backoff.on_exception(backoff.expo, (PyMongoError, ), max_tries=20, max_time=120)
    async def update_one(self, collection: str, _id: UUID, obj: dict | BaseModel):
        upd_obj = obj
        if isinstance(upd_obj, BaseModel):
            upd_obj = upd_obj.dict()
        if not '_id':
            raise ValueError('_id must be specified')

        obj_id = str(_id)
        collection_orm = await self.__get_collection(collection)
        result_obj = await collection_orm.find_one_and_update(
            {'_id': obj_id},
            {'$set': upd_obj},
            return_document=ReturnDocument.AFTER
        )
        return result_obj

    @backoff.on_exception(backoff.expo, (PyMongoError, ), max_tries=20, max_time=120)
    async def find(self, collection: str, page: int = 1, limit: int = 10, filter: dict = None):
        if filter is None:
            filter = {}
        collection_orm = await self.__get_collection(collection)
        result_objects = []
        cursor = collection_orm.find(filter).skip((page - 1) * limit).limit(limit)
        for document in await cursor.to_list(limit):
            result_objects.append(document)
        return result_objects

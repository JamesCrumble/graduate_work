from bson import ObjectId
from db.baseinterface import DbInterface
from db.managers import mongo_context


class MongoManager(DbInterface):
    INTERFACE_NAME = 'MongoDB'

    def prepare(self):
        pass

    def write(self, modelclass, data: dict):
        with mongo_context() as mongo_client:
            db = mongo_client['mydatabase']
            collection = db['mycollection']
            result = collection.insert_one(data)
        return result.inserted_id

    def read(self, data: ObjectId):
        with mongo_context() as mongo_client:
            db = mongo_client['mydatabase']
            collection = db['mycollection']
            return collection.find_one({'_id': data})

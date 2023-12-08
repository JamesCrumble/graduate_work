from db.mongo import MongoManager
from db.postgres import PgManager

db_list = [
    MongoManager,
    PgManager,
]

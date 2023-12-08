from db.baseinterface import DbInterface
from db.managers import pg_context
from models.postgres import tables


class PgManager(DbInterface):
    INTERFACE_NAME = 'Postgres'

    def prepare(self):
        with pg_context() as [pgconn, pg_cursor]:
            pg_cursor.execute('DROP SCHEMA IF EXISTS content CASCADE;')
            pg_cursor.execute('CREATE SCHEMA content;')
            for item in tables.values():
                pg_cursor.execute(item['sqlc'])
            pgconn.commit()

    def write(self, modelclass, data: dict):
        id: int = None
        values = tuple(data[i] for i in tables[modelclass]['data'])
        with pg_context() as [pgconn, pg_cursor]:
            args = pg_cursor.mogrify(tables[modelclass]['sqlm'], values).decode('utf-8')
            pg_cursor.execute(tables[modelclass]['sqli'] + (args))
            id = pg_cursor.fetchone()[0]
            pgconn.commit()
        return (modelclass, id,)

    def read(self, data: tuple):
        modelclass = data[0]
        with pg_context() as [pgconn, pg_cursor]:
            pg_cursor.execute(tables[modelclass]['sqls'] + str(data[1])+';')
            result = pg_cursor.fetchone()[0]
        return result

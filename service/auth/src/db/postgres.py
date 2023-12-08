from settings import settings
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def get_postgres_engine() -> AsyncEngine:
    dsl = {
        'dbname': settings.postgres_db,
        'user': settings.postgres_user,
        'password': settings.postgres_password,
        'host': settings.postgres_host,
        'port': settings.postgres_port,
    }
    connection_string = (
        'postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}'
    ).format(
        **dsl,
    )
    engine = create_async_engine(
        connection_string,
    )
    return engine


service_session_maker = async_sessionmaker(
    bind=get_postgres_engine(),
    autocommit=False,
    autoflush=False,
    future=True,
)


# Dependency
async def service_session() -> AsyncSession:
    async with service_session_maker() as session:
        yield session

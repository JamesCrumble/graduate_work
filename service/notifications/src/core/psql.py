from settings import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

sync_service_engine = create_engine(
    f'postgresql+psycopg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}/{settings.postgres_db}',
    echo=settings.echo,
    connect_args={'connect_timeout': 120},
)
sync_service_session_maker = sessionmaker(
    bind=sync_service_engine,
    autocommit=False,
    autoflush=False,
)

async_service_engine = create_async_engine(
    f'postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}/{settings.postgres_db}',
    echo=settings.echo,
)
async_service_session_maker = async_sessionmaker(
    bind=async_service_engine,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

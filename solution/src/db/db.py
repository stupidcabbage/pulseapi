from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import postgres_settings

engine = create_async_engine(f"postgresql+asyncpg://{postgres_settings.POSTGRES_USERNAME}:{postgres_settings.POSTGRES_PASSWORD}@{postgres_settings.POSTGRES_HOST}:{postgres_settings.POSTGRES_PORT}/{postgres_settings.POSTGRES_DATABASE}")

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session

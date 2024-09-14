from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from model import BaseClass

engine = create_async_engine("postgresql+asyncpg://postgres:1@localhost:5432/postgres", pool_pre_ping=True,
    pool_recycle=3600)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseClass.metadata.create_all)


async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session(self):
    async with self.session_maker() as session:
        yield session

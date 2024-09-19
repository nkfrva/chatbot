from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os
from dotenv import load_dotenv
from model import BaseClass


load_dotenv()
engine = create_async_engine(os.getenv(os.environ.get("CONNECTION_STRING")), pool_pre_ping=True, pool_recycle=3600)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseClass.metadata.create_all)


async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@asynccontextmanager
async def get_session():
    async with async_session_maker() as session:
        yield session

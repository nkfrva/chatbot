import uuid
from typing import Any

from sqlmodel import select
from sqlmodel import Session

from model.key import Key
from config.init_db import get_session


class KeyRepository:
    async def get_keys(self) -> list[Key]:
        async with get_session() as session:
            result = await session.scalars(select(Key))
            return result.scalars().all()

    async def get_key_by_id(self, key_id: uuid.UUID) -> Key:
        async with get_session() as session:
            result = await session.get(Key, key_id)
            return result


    async def get_key_id_by_key(self, key_title: str) -> Any:
        async with get_session() as session:
            result = await session.execute(select(Key).where(Key.key == key_title))
            key = result.scalars().first()
            return key.uuid


    async def create_key(self, new_key: Key) -> Key:
        async with get_session() as session:
            session.add(new_key)
            await session.commit()
            await session.refresh(new_key)
            return new_key

    async def delete_key_by_id(self, key_id: uuid.UUID) -> bool:
        async with get_session() as session:
            result = await session.get(Key, key_id)

            if result is None:
                return False

            await session.delete(result)
            await session.commit()
            return True
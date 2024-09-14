import uuid

from sqlmodel import select
from sqlmodel import Session

from model.key import Key
from config.init_db import get_session


class KeyRepository:
    async def get_keys(self) -> list[Key]:
        async with get_session() as session:
            result = await session.scalars(select(Key)).all()
            return [Key(uuid=key.uuid,
                        key=key.key,
                        task_uuid=key.task_uuid) for key in result]

    async def get_key_by_id(self, key_id: uuid.UUID) -> Key:
        async with get_session() as session:
            result = await session.get(Key, key_id)
            return result

    async def create_key(self, key_create: dict, task_uuid: uuid) -> Key:
        async with get_session() as session:
            new_key = Key(key=key_create["key"],
                          task_uuid=task_uuid)

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
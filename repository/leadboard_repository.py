import uuid
from sqlmodel import select

from model.leadboard import LeadBoard
from config.init_db import get_session


class LeadboardRepository:

    @staticmethod
    async def get_entries_from_leadboard() -> list[LeadBoard]:
        async with get_session() as session:
            result = await session.execute(select(LeadBoard))
            return result.scalars().all()

    @staticmethod
    async def get_leadboard_entry_by_id(entry_id: uuid.UUID) -> LeadBoard:
        async with get_session() as session:
            result = await session.get(LeadBoard, entry_id)
            return result

    @staticmethod
    async def get_leadboard_id_by_team_id(team_id: uuid.UUID) -> uuid.UUID:
        async with get_session() as session:
            result = await session.execute(select(LeadBoard).where(LeadBoard.team_uuid == team_id))
            leadboard = result.scalars().first()
            return leadboard.uuid

    # region CRUD

    @staticmethod
    async def create_leadboard_entry(new_entry: LeadBoard) -> LeadBoard:
        async with get_session() as session:
            session.add(new_entry)
            await session.commit()
            await session.refresh(new_entry)
            return new_entry

    @staticmethod
    async def update_leadboard_entry(leadboard_id: uuid.UUID, **kwargs) -> LeadBoard:
        async with get_session() as session:
            leadboard = await LeadboardRepository.get_leadboard_entry_by_id(leadboard_id)
            if not leadboard:
                return None

            for key, value in kwargs.items():
                setattr(leadboard, key, value)

            session.add(leadboard)
            await session.commit()
            await session.refresh(leadboard)
            return leadboard

    @staticmethod
    async def delete_leadboard_entry_by_id(entry_id: uuid.UUID) -> bool:
        async with get_session() as session:
            result = await session.get(LeadBoard, entry_id)
            if result is None:
                return False
            await session.delete(result)
            await session.commit()
            return True

    # endregion

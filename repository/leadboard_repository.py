import uuid

from sqlmodel import select
from sqlmodel import Session

from model.leadboard import LeadBoard
from config.init_db import get_session


class LeadBoardRepository:
    class LeadBoardRepository:
        async def get_entries_from_leadboard(self) -> list[LeadBoard]:
            async with get_session() as session:
                result = await session.exec(select(LeadBoard)).all()
                return [LeadBoard(uuid=team_entries.uuid,
                                  key=team_entries.key,
                                  team_uuid=team_entries.team_uuid,
                                  points=team_entries.points) for team_entries in result]

        async def create_entry(self, entry_create: dict, team_uuid: uuid.UUID) -> LeadBoard:
            async with get_session() as session:
                new_entry = LeadBoard(key=entry_create["key"],
                                      team_uuid=team_uuid,
                                      points=entry_create["points"])
                session.add(new_entry)
                await session.commit()
                await session.refresh(new_entry)
                return new_entry

        async def delete_entry_by_id(self, entry_id: uuid.UUID) -> bool:
            async with get_session() as session:
                result = await session.get(LeadBoard, entry_id)
                if result is None:
                    return False
                await session.delete(result)
                await session.commit()
                return True

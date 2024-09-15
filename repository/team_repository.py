import uuid
from typing import Any

from sqlmodel import select
from sqlmodel import Session

from model.team import Team
from config.init_db import get_session


class TeamRepository:
    async def get_teams(self) -> list[Team]:
        async with get_session() as session:
            result = await session.exec(select(Team))
            return result.scalars().all()

    async def get_team_by_id(self, team_id: uuid.UUID) -> Team:
        async with get_session() as session:
            result = await session.get(Team, team_id)
            return result

    async def get_team_id_by_name(self, team_name: str) -> Any:
        async with get_session() as session:
            result = await session.execute(select(Team).where(Team.name == team_name))
            team = result.scalars().first()
            return team.uuid

    async def create_team(self, new_team: Team) -> Team:
        async with get_session() as session:
            session.add(new_team)
            await session.commit()
            await session.refresh(new_team)
            return new_team

    async def delete_team_by_id(self, team_id: uuid.UUID) -> bool:
        async with get_session() as session:
            result = await session.get(Team, team_id)

            if result is None:
                return False

            await session.delete(result)
            await session.commit()
            return True

    # def get_teams(self) -> list[Team]:
    #     session: Session = next(get_session())
    #     result = session.scalars(select(Team)).all()
    #     session.close()
    #     return [Team(uuid=team.uuid,
    #                  key=team.key,
    #                  name=team.name,
    #                  team_statistic_uuid=team.team_statistic_uuid) for team in result]
    #
    # def get_team_by_id(self, team_id: uuid.UUID) -> Team:
    #     session: Session = next(get_session())
    #     result = session.get(Team, team_id)
    #     session.close()
    #     return result
    #
    # def create_team(self, team_create: Team, team_statistic_uuid: uuid) -> Team:
    #     session: Session = next(get_session())
    #     new_team = Team(key=team_create["key"],
    #                   name=team_create["name"],
    #                   team_statistic_uuid=team_statistic_uuid)
    #
    #     session.add(new_team)
    #     session.commit()
    #     session.refresh(new_team)
    #     session.close()
    #     return new_team
    #
    # def delete_team_by_id(self, team_id: uuid.UUID) -> bool:
    #     session: Session = next(get_session())
    #     result = session.get(Team, team_id)
    #
    #     if result is None:
    #         return False
    #
    #     session.delete(result)
    #     session.commit()
    #     session.close()
    #     return True

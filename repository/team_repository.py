import uuid
from sqlmodel import select
import csv

from model.team import Team
from config.init_db import get_session
from config.csv_format import CSV_team, get_key_pairs


class TeamRepository:

    @staticmethod
    async def get_teams() -> list[Team]:
        async with get_session() as session:
            result = await session.execute(select(Team))
            return result.scalars().all()

    @staticmethod
    async def get_team_by_id(team_id: uuid.UUID) -> Team:
        async with get_session() as session:
            result = await session.get(Team, team_id)
            return result

    @staticmethod
    async def get_team_id_by_token(team_token: str) -> uuid:
        async with get_session() as session:
            result = await session.execute(select(Team.uuid).where(Team.key == team_token))
            team = result.scalars().first()
            return team

    @staticmethod
    async def get_team_id_by_name(team_name: str) -> uuid:
        async with get_session() as session:
            result = await session.execute(select(Team.uuid).where(Team.name == team_name))
            team = result.scalars().first()
            return team

    @staticmethod
    async def get_full_team_id_by_name(team_name: str):
        async with get_session() as session:
            result = await session.execute(select(Team).where(Team.name == team_name))
            team = result.scalars().first()
            return team

    @staticmethod
    async def ban_team_by_uuid(uuid):
        async with get_session() as session:
            result = await session.execute(select(Team).where(Team.uuid == uuid))
            team = result.scalars().first()

            new_value = not team.ban
            team.ban = new_value

            await session.commit()
            await session.refresh(team)
            return new_value

    # region CRUD

    @staticmethod
    async def create_team(new_team: Team) -> Team:
        async with get_session() as session:
            session.add(new_team)
            await session.commit()
            await session.refresh(new_team)
            return new_team

    @staticmethod
    async def delete_team_by_id(team_id: uuid.UUID) -> bool:
        async with get_session() as session:
            result = await session.get(Team, team_id)

            if result is None:
                return False

            await session.delete(result)
            await session.commit()
            return True

    # endregion

    # region import from csv

    @staticmethod
    async def import_from_csv(filepath: str):
        with open(filepath, 'r', encoding='windows-1251') as file:
            reader = csv.DictReader(file)
            async with get_session() as session:
                for row in reader:
                    pairs = get_key_pairs(row)
                    team = Team(name=pairs[CSV_team.name], ban=False)
                    session.add(team)
                    await session.commit()
                    await session.refresh(team)

    # endregion

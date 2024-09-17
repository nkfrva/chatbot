import uuid
from sqlmodel import select

from model.team_statistic import TeamStatistic
from config.init_db import get_session


class TeamStatisticRepository:

    @staticmethod
    async def get_team_statistics() -> list[TeamStatistic]:
        async with get_session() as session:
            result = await session.execute(select(TeamStatistic))
            return result.scalars().all()

    @staticmethod
    async def get_team_statistic_by_id(team_statistic_id: uuid.UUID) -> TeamStatistic:
        async with get_session() as session:
            result = await session.get(TeamStatistic, team_statistic_id)
            return result

    @staticmethod
    async def get_passed_stations_by_team_id(team_id: uuid.UUID) -> list[TeamStatistic]:
        async with get_session() as session:
            result = await session.execute(select(TeamStatistic).where(TeamStatistic.team_uuid == team_id))
            statistics = result.scalars().all()
            return statistics

    @staticmethod
    async def get_statistic_id_by_team_id_station_id(team_id: uuid.UUID, station_id: uuid.UUID) -> TeamStatistic:
        async with get_session() as session:
            result = await session.execute(select(TeamStatistic).where((TeamStatistic.team_uuid == team_id)
                                                                       & (TeamStatistic.station_uuid == station_id)))
            statistic = result.scalars().first()
            return statistic

    # region CRUD

    @staticmethod
    async def create_team_statistic(new_statistic: TeamStatistic) -> TeamStatistic:
        async with get_session() as session:
            session.add(new_statistic)
            await session.commit()
            await session.refresh(new_statistic)
            return new_statistic

    @staticmethod
    async def update_team_statistic(statistic_id: uuid.UUID, **kwargs) -> TeamStatistic:
        async with get_session() as session:
            statistic = await TeamStatisticRepository.get_team_statistic_by_id(statistic_id)
            if not statistic:
                return None

            for key, value in kwargs.items():
                setattr(statistic, key, value)

            session.add(statistic)
            await session.commit()
            await session.refresh(statistic)
            return statistic

    @staticmethod
    async def delete_team_statistic_by_id(team_statistic_id: uuid.UUID) -> bool:
        async with get_session() as session:
            result = await session.get(TeamStatistic, team_statistic_id)

            if result is None:
                return False

            await session.delete(result)
            await session.commit()
            return True

    # endregion

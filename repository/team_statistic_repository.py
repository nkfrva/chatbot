import uuid

from sqlmodel import select
from sqlmodel import Session

from model.team_statistic import TeamStatistic
from config.init_db import get_session


class TeamStatisticRepository:
    async def get_team_statistics(self) -> list[TeamStatistic]:
        async with get_session() as session:
            result = await session.execute(select(TeamStatistic))
            return result.scalars().all()

    async def get_team_statistic_by_id(self, team_statistic_id: uuid.UUID) -> TeamStatistic:
        async with get_session() as session:
            result = await session.get(TeamStatistic, team_statistic_id)
            return result

    async def get_passed_stations_by_team_id(self, team_id: uuid.UUID) -> list[TeamStatistic]:
        async with get_session() as session:
            result = await session.execute(select(TeamStatistic).where(TeamStatistic.team_uuid == team_id))
            statistics = result.scalars().all()
            return statistics

    async def get_statistic_id_by_team_id_station_id(self, team_id: uuid.UUID, station_id: uuid.UUID) -> TeamStatistic:
        async with get_session() as session:
            result = await session.execute(select(TeamStatistic).where((TeamStatistic.team_uuid == team_id)
                                                                       & (TeamStatistic.station_uuid == station_id)))
            statistic = result.scalars().first()
            return statistic

    async def create_team_statistic(self, new_statistic: TeamStatistic) -> TeamStatistic:
        async with get_session() as session:
            session.add(new_statistic)
            await session.commit()
            await session.refresh(new_statistic)
            return new_statistic

    async def update_team_statistic(self, statistic_id: uuid.UUID, **kwargs) -> TeamStatistic:
        async with get_session() as session:
            statistic = await self.get_team_statistic_by_id(statistic_id)
            if not statistic:
                return None

            for key, value in kwargs.items():
                setattr(statistic, key, value)

            session.add(statistic)
            await session.commit()
            await session.refresh(statistic)
            return statistic

    async def delete_team_statistic_by_id(self, team_statistic_id: uuid.UUID) -> bool:
        async with get_session() as session:
            result = await session.get(TeamStatistic, team_statistic_id)

            if result is None:
                return False

            await session.delete(result)
            await session.commit()
            return True

    # def get_team_statistics(self) -> list[TeamStatistic]:
    #     session: Session = next(get_session())
    #     result = session.scalars(select(TeamStatistic)).all()
    #     session.close()
    #     return [TeamStatistic(uuid=team_statistic.uuid,
    #                           point=team_statistic.point,
    #                           team_uuid=team_statistic.team_uuid) for team_statistic in result]
    #
    # def get_team_statistic_by_id(self, team_statistic_id: uuid.UUID) -> TeamStatistic:
    #     session: Session = next(get_session())
    #     result = session.get(TeamStatistic, team_statistic_id)
    #     session.close()
    #     return result
    #
    # def create_team_statistic(self, statistic_create: TeamStatistic, team_uuid: uuid) -> TeamStatistic:
    #     session: Session = next(get_session())
    #     new_statistic = TeamStatistic(point=statistic_create["point"],
    #                   team_uuid=team_uuid)
    #
    #     session.add(new_statistic)
    #     session.commit()
    #     session.refresh(new_statistic)
    #     session.close()
    #     return new_statistic
    #
    # def delete_team_statistic_by_id(self, team_statistic_id: uuid.UUID) -> bool:
    #     session: Session = next(get_session())
    #     result = session.get(TeamStatistic, team_statistic_id)
    #
    #     if result is None:
    #         return False
    #
    #     session.delete(result)
    #     session.commit()
    #     session.close()
    #     return True

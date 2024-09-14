import uuid

from sqlmodel import select
from sqlmodel import Session

from model.team_statistic import TeamStatistic
from config.init_db import get_session


class TeamStatisticRepository:
    async def get_team_statistics(self) -> list[TeamStatistic]:
        async with get_session() as session:
            result = await session.exec(select(TeamStatistic)).all()
            return [TeamStatistic(uuid=team_statistic.uuid,
                                  point=team_statistic.point,
                                  team_uuid=team_statistic.team_uuid) for team_statistic in result]

    async def get_team_statistic_by_id(self, team_statistic_id: uuid.UUID) -> TeamStatistic:
        async with get_session() as session:
            result = await session.get(TeamStatistic, team_statistic_id)
            return result

    async def create_team_statistic(self, statistic_create: dict, team_uuid: uuid.UUID) -> TeamStatistic:
        async with get_session() as session:
            new_statistic = TeamStatistic(point=statistic_create["point"],
                                          team_uuid=team_uuid)

            session.add(new_statistic)
            await session.commit()
            await session.refresh(new_statistic)
            return new_statistic

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

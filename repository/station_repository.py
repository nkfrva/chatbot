import uuid

from sqlmodel import select
from sqlmodel import Session

from model.station import Station
from config.init_db import get_session


class StationRepository:
    async def get_stations(self) -> list[Station]:
        async with get_session() as session:
            result = await session.exec(select(Station)).all()
            return [Station(uuid=station.uuid,
                            title=station.title,
                            description=station.description) for station in result]

    async def get_station_by_id(self, station_id: uuid.UUID) -> Station:
        async with get_session() as session:
            result = await session.get(Station, station_id)
            return result

    # def get_stations(self) -> list[Station]:
    #     session: Session = next(get_session())
    #     result = session.scalars(select(Station)).all()
    #     session.close()
    #     return [Station(uuid=station.uuid,
    #                     title=station.title,
    #                     description=station.description) for station in result]
    #
    # def get_station_by_id(self, station_id: uuid.UUID) -> Station:
    #     session: Session = next(get_session())
    #     result = session.get(Station, station_id)
    #     session.close()
    #     return result


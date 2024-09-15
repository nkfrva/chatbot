import uuid

from sqlmodel import select, update
from sqlmodel import Session

from model.station import Station
from config.init_db import get_session


class StationRepository:
    async def get_stations(self) -> list[Station]:
        async with get_session() as session:
            result = await session.exec(select(Station))
            return result.scalars().all()

    async def get_station_by_id(self, station_id: uuid.UUID) -> Station:
        async with get_session() as session:
            result = await session.get(Station, station_id)
            return result

    async def update_station(self, station_id: uuid.UUID, **kwargs) -> Station:
        async with get_session() as session:
            # Retrieve the existing station
            station = await self.get_station_by_id(station_id)
            if not station:
                return None

            for key, value in kwargs.items():
                setattr(station, key, value)

            session.add(station)
            await session.commit()
            await session.refresh(station)
            return station

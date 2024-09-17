import uuid
from typing import Any

from sqlmodel import select, update
from sqlmodel import Session

from model.station import Station
from config.init_db import get_session


class StationRepository:
    async def get_stations(self) -> list[Station]:
        async with get_session() as session:
            result = await session.execute(select(Station))
            return result.scalars().all()

    async def get_station_by_id(self, station_id: uuid.UUID) -> Station:
        async with get_session() as session:
            result = await session.get(Station, station_id)
            return result

    async def get_station_by_team_uuid(self, team_uuid: uuid.UUID) -> Station:
        async with get_session() as session:
            result = await session.execute(select(Station).where(Station.team_uuid == team_uuid))
            if result:
                station = result.scalars().first()
                return station
            else:
                return None

    async def get_station_id_by_title(self, station_title: str) -> Any:
        async with get_session() as session:
            result = await session.execute(select(Station).where(Station.title == station_title))
            task = result.scalars().first()
            return task.uuid

    async def create_station(self, new_station: Station) -> Station:
        async with get_session() as session:
            session.add(new_station)
            await session.commit()
            await session.refresh(new_station)
            return new_station

    async def update_station(self, station_id: uuid.UUID, **kwargs) -> Station:
        async with get_session() as session:
            station = await self.get_station_by_id(station_id)
            if not station:
                return None

            for key, value in kwargs.items():
                setattr(station, key, value)

            session.add(station)
            await session.commit()
            await session.refresh(station)
            return station

    async def delete_station_by_id(self, station_id: uuid.UUID) -> bool:
        async with get_session() as session:
            result = await session.get(Station, station_id)

            if result is None:
                return False

            await session.delete(result)
            await session.commit()
            return True

import uuid
import csv
from sqlmodel import select

from config.init_db import get_session
from model.station import Station
from config.csv_format import CSV_station, get_key_pairs
from repository.task_repository import TaskRepository


class StationRepository:

    @staticmethod
    async def get_stations() -> list[Station]:
        async with get_session() as session:
            result = await session.execute(select(Station))
            return result.scalars().all()

    @staticmethod
    async def get_station_by_id(station_id: uuid.UUID) -> Station:
        async with get_session() as session:
            result = await session.get(Station, station_id)
            return result

    @staticmethod
    async def get_station_by_team_uuid(team_uuid: uuid.UUID) -> Station:
        async with get_session() as session:
            result = await session.execute(select(Station).where(Station.team_uuid == team_uuid))
            if result:
                station = result.scalars().first()
                return station
            else:
                return None

    @staticmethod
    async def get_station_id_by_title(station_title: str):
        async with get_session() as session:
            result = await session.execute(select(Station).where(Station.title == station_title))
            station = result.scalars().first()
            return station


    # region CRUD
    @staticmethod
    async def create_station(new_station: Station) -> Station:
        async with get_session() as session:
            session.add(new_station)
            await session.commit()
            await session.refresh(new_station)
            return new_station

    @staticmethod
    async def update_station(station_id: uuid.UUID, **kwargs) -> Station:
        async with get_session() as session:
            station = await StationRepository.get_station_by_id(station_id)
            if not station:
                return None

            for key, value in kwargs.items():
                setattr(station, key, value)

            session.add(station)
            await session.commit()
            await session.refresh(station)
            return station

    @staticmethod
    async def delete_station_by_id(station_id: uuid.UUID) -> bool:
        async with get_session() as session:
            result = await session.get(Station, station_id)

            if result is None:
                return False

            await session.delete(result)
            await session.commit()
            return True

    # endregion

    # region import from csv

    @staticmethod
    async def import_from_csv(filepath):
        with open(filepath, 'r', encoding='windows-1251') as file:
            reader = csv.DictReader(file)
            task_repository = TaskRepository()
            tasks = await task_repository.get_tasks()

            async with get_session() as session:
                for row in reader:
                    pairs = get_key_pairs(row)
                    task = [t for t in tasks if t.title == pairs[CSV_station.key]][0]
                    team = Station(title=pairs[CSV_station.title],
                                   description=pairs[CSV_station.description],
                                   task_uuid=task.uuid)
                    session.add(team)
                    await session.commit()
                    await session.refresh(team)

    # endregion

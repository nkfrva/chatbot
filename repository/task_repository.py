import uuid
from sqlmodel import select
import csv

from model.task import Task
from config.init_db import get_session
from config.csv_format import CSV_task, get_key_pairs


class TaskRepository:

    @staticmethod
    async def get_tasks() -> list[Task]:
        async with get_session() as session:
            result = await session.execute(select(Task))
            return result.scalars().all()

    @staticmethod
    async def get_task_by_id(task_id: uuid.UUID) -> Task:
        async with get_session() as session:
            result = await session.get(Task, task_id)
            return result

    @staticmethod
    async def get_task_id_by_title(task_title: str):
        async with get_session() as session:
            result = await session.execute(select(Task).where(Task.title == task_title))
            task = result.scalars().first()
            return task

    # region CRUD

    @staticmethod
    async def create_task(new_task: Task) -> Task:
        async with get_session() as session:
            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)
            return new_task

    @staticmethod
    async def delete_task_by_id(task_id: uuid.UUID) -> bool:
        async with get_session() as session:
            result = await session.get(Task, task_id)

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
            async with get_session() as session:
                for row in reader:
                    print(row)
                    pairs = get_key_pairs(row)
                    task = Task(title=pairs[CSV_task.title],
                                description=pairs[CSV_task.description],
                                key=pairs[CSV_task.key])
                    session.add(task)
                    await session.commit()
                    await session.refresh(task)

    # endregion

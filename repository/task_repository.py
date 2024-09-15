import uuid

from sqlmodel import select
from sqlmodel import Session

from model.task import Task
from config.init_db import get_session


class TaskRepository:
    async def get_tasks(self) -> list[Task]:
        async with get_session() as session:
            result = await session.exec(select(Task))
            return result.scalars().all()

    async def get_task_by_id(self, task_id: uuid.UUID) -> Task:
        async with get_session() as session:
            result = await session.get(Task, task_id)
            return result

    async def create_task(self, task_create: dict, key_uuid: uuid.UUID) -> Task:
        async with get_session() as session:
            new_task = Task(title=task_create["title"],
                            description=task_create["description"],
                            key_uuid=key_uuid)

            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)
            return new_task

    async def delete_task_by_id(self, task_id: uuid.UUID) -> bool:
        async with get_session() as session:
            result = await session.get(Task, task_id)

            if result is None:
                return False

            await session.delete(result)
            await session.commit()
            return True

    # def get_tasks(self) -> list[Task]:
    #     session: Session = next(get_session())
    #     result = session.scalars(select(Task)).all()
    #     session.close()
    #     return [Task(uuid=task.uuid,
    #                  title=task.title,
    #                  description=task.description,
    #                  key_uuid=task.key_uuid) for task in result]
    #
    # def get_task_by_id(self, task_id: uuid.UUID) -> Task:
    #     session: Session = next(get_session())
    #     result = session.get(Task, task_id)
    #     session.close()
    #     return result
    #
    # def create_task(self, task_create: Task, key_uuid: uuid) -> Task:
    #     session: Session = next(get_session())
    #     new_task = Task(title=task_create["title"],
    #                   description=task_create["description"],
    #                   key_uuid=key_uuid)
    #
    #     session.add(new_task)
    #     session.commit()
    #     session.refresh(new_task)
    #     session.close()
    #     return new_task
    #
    # def delete_task_by_id(self, task_id: uuid.UUID) -> bool:
    #     session: Session = next(get_session())
    #     result = session.get(Task, task_id)
    #
    #     if result is None:
    #         return False
    #
    #     session.delete(result)
    #     session.commit()
    #     session.close()
    #     return True

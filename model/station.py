from uuid import uuid4
from sqlalchemy import Column, Integer, String, ForeignKey, UUID, Boolean, CheckConstraint
from .base_class import BaseClass
from sqlalchemy.orm import relationship

class Station(BaseClass):

    __tablename__ = 'station'

    uuid: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=True)
    title: str = Column(String, default="student", nullable=False)
    description: str = Column(String, default="student", nullable=False)

    team_uuid: UUID = Column(UUID, ForeignKey("team.uuid"), nullable=True, index=True)
    team = relationship("Team", back_populates="stations", uselist=False)

    task_uuid: UUID = Column(UUID, ForeignKey("task.uuid"), nullable=True, index=True)
    tasks = relationship("Task", back_populates="stations", uselist=False)

    team_statistic = relationship("TeamStatistic", back_populates="stations", uselist=False)

    # key_uuid: UUID = Column(UUID, ForeignKey("key.uuid"), nullable=False, index=True)
    # keys = relationship("Key", back_populates="tasks", uselist=False)

    # max time - добавить максимальное время на станции
    # организаторам добавить возможность освободить станцию
    # если команда игнориурет станцию - мы ее временно блокируем (сценарий взять у оргов)

    # TODO добавить очки за станцию, кол-во командр, которые станцию прошли (опционально)


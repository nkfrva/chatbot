from uuid import uuid4
from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
from .base_class import BaseClass


# TODO добавить связи с задачами
class Task(BaseClass):

    __tablename__ = 'task'

    uuid: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=True)
    title: str = Column(String, default="student", nullable=False)
    description: str = Column(String, default="student", nullable=False)
    key: str = Column(String, default="key", nullable=False)

    stations = relationship("Station", back_populates="tasks", uselist=False)
    # # хранит uuid ответа
    # key_uuid: UUID = Column(UUID, ForeignKey("key.uuid"), nullable=False, index=True)
    # keys = relationship("Key", back_populates="tasks", uselist=False)

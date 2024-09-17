from uuid import uuid4
from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
from .base_class import BaseClass


class Task(BaseClass):

    __tablename__ = 'task'

    uuid: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=True)
    title: str = Column(String, default="student", nullable=False)
    description: str = Column(String, default="student", nullable=False)
    key: str = Column(String, default="key", nullable=False)

    stations = relationship("Station", back_populates="tasks", uselist=False)

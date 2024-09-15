from uuid import uuid4
from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
from .base_class import BaseClass

# TODO добавить связи с задачами
class Key(BaseClass):

    __tablename__ = 'key'

    uuid: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=True)
    key: str = Column(String, default="Loxi", nullable=False)

    # один к одному
    # не хранит uuid задания!!!!
    tasks = relationship("Task", back_populates="keys", uselist=False)
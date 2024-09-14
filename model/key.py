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
    task_uuid: UUID = Column(UUID, ForeignKey("task.uuid"), nullable=False, index=True)
    #task = relationship("Task", back_populates="key", uselist=False)

from uuid import uuid4
from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
from .base_class import BaseClass


class Command(BaseClass):

    __tablename__ = 'command'

    uuid: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=True)
    title: str = Column(String, default="Loxi", nullable=False)
    description: str = Column(String, default="Loxi", nullable=False)
    action: str = Column(String, default="Loxi", nullable=False)

    # много команд - одна роль
    role_uuid: UUID = Column(UUID, ForeignKey("role.uuid"), nullable=False, index=True)
    role = relationship("Role", back_populates="commands")

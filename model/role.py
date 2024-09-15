from uuid import uuid4
from sqlalchemy import Column, Integer, String, ForeignKey, UUID, Boolean, CheckConstraint
from .base_class import BaseClass
from sqlalchemy.orm import relationship

class Role(BaseClass):

    __tablename__ = 'role'

    uuid: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=True)
    title: str = Column(String, default="student", nullable=False)

    # одна роль - много команд/участников
    # команда никак не связана с ролями
    commands = relationship("Command", back_populates="roles", cascade="delete")

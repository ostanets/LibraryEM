from enum import Enum

from sqlalchemy import Column, Integer, String
from . import Base


class Status(Base):
    __tablename__ = 'statuses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)


class Statuses(Enum):
    AVAILABLE = "в наличии"
    BORROWED = "выдана"

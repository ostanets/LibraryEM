from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import DATABASE_URL
from .models import Base


class Database:
    _engine = create_engine(DATABASE_URL)
    _session_local = ...

    @classmethod
    def init_db(cls):
        Base.metadata.create_all(bind=cls._engine)
        cls._session_local = sessionmaker(autocommit=False, autoflush=False, bind=cls._engine)

    @classmethod
    def get_session(cls) -> Session:
        return cls._session_local()

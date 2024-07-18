import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from logging_config import configure_logging
from repo.models import Base
from repo.repo import Repo
from repo.models.status import Statuses, Status

configure_logging()

DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture()
def session():
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(bind=engine)
    _sessionmaker = sessionmaker(bind=engine)
    session: Session = _sessionmaker()

    yield session

    session.close()
    engine.dispose()


def assert_statuses_exist(session: Session):
    available_status = session.query(Status).filter_by(name=Statuses.AVAILABLE.value).first()
    borrowed_status = session.query(Status).filter_by(name=Statuses.BORROWED.value).first()

    assert available_status is not None
    assert borrowed_status is not None


def test_create_base_statuses(session: Session):
    repo = Repo(session)

    repo.create_base_statuses()
    assert_statuses_exist(session)


def test_create_base_statuses_partially_exists(session: Session):
    repo = Repo(session)

    session.add(Status(name=Statuses.AVAILABLE.value))
    session.commit()

    repo.create_base_statuses()

    assert_statuses_exist(session)


def test_create_base_statuses_already_exists(session: Session):
    repo = Repo(session)

    session.add_all([
        Status(name=Statuses.AVAILABLE.value),
        Status(name=Statuses.BORROWED.value)
    ])
    session.commit()

    repo.create_base_statuses()

    assert_statuses_exist(session)

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from logging_config import configure_logging
from repo.models import Base
from repo.models.book import Book
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
    available_status = session.query(Status).filter_by(name=Statuses.AVAILABLE.name).first()
    borrowed_status = session.query(Status).filter_by(name=Statuses.BORROWED.name).first()

    assert available_status is not None
    assert borrowed_status is not None


def test_create_base_statuses(session: Session):
    repo = Repo(session)

    repo.create_base_statuses()
    assert_statuses_exist(session)


def test_create_base_statuses_partially_exists(session: Session):
    repo = Repo(session)

    session.add(Status(name=Statuses.AVAILABLE.name))
    session.commit()

    repo.create_base_statuses()

    assert_statuses_exist(session)


def test_create_base_statuses_already_exists(session: Session):
    repo = Repo(session)

    session.add_all([
        Status(name=Statuses.AVAILABLE.name),
        Status(name=Statuses.BORROWED.name)
    ])
    session.commit()

    repo.create_base_statuses()

    assert_statuses_exist(session)


def test_get_statuses(session: Session):
    repo = Repo(session)

    session.add_all([
        Status(name=Statuses.AVAILABLE.name),
        Status(name=Statuses.BORROWED.name)
    ])

    session.commit()

    statuses = repo.get_statuses()
    assert len(statuses) == 2


def test_get_status_id(session: Session):
    repo = Repo(session)

    session.add(Status(name="test"))

    session.commit()

    exist_status = repo.get_status_id("test")
    not_exist_status = repo.get_status_id("1234")

    assert exist_status is not None
    assert not_exist_status is None


def test_add_a_book(session: Session):
    repo = Repo(session)

    repo.create_base_statuses()

    book = Book(title="test_title", author="test_author", year=2024, status_id=Statuses.AVAILABLE.value)
    inserted_book_id = repo.add_a_book(book)
    assert book.id == inserted_book_id

    fetched_book: Book = session.query(Book).filter_by(title="test_title").first()

    assert fetched_book is not None
    assert fetched_book.id == inserted_book_id


def test_find_books_by_query(session: Session):
    repo = Repo(session)
    repo.create_base_statuses()

    book = Book(title="test_title", author="test_author", year=2024, status_id=Statuses.AVAILABLE.value)
    repo.add_a_book(book)

    found_books_by_title: list[Book] = repo.find_books("test_title")
    assert len(found_books_by_title) == 1

    found_books_by_author: list[Book] = repo.find_books("test_author")
    assert len(found_books_by_author) == 1

    found_books_by_year: list[Book] = repo.find_books("2024")
    assert len(found_books_by_year) == 1


def test_find_all_books(session: Session):
    repo = Repo(session)
    repo.create_base_statuses()

    book = Book(title="1", author="test_author", year=2024, status_id=Statuses.AVAILABLE.value)
    repo.add_a_book(book)

    book = Book(title="2", author="test_author", year=2022, status_id=Statuses.AVAILABLE.value)
    repo.add_a_book(book)

    found_books: list[Book] = repo.find_books()

    assert len(found_books) == 2


def test_edit_book_status(session: Session):
    repo = Repo(session)
    repo.create_base_statuses()

    book = Book(title="1", author="test_author", year=2024, status_id=Statuses.AVAILABLE.value)
    repo.add_a_book(book)

    op_result = repo.edit_book_status(book.id, Statuses.BORROWED)
    assert op_result

    found_books: list[Book] = repo.find_books("1")

    assert found_books[0].status.name == Statuses.BORROWED.name


def test_remove_a_book(session: Session):
    repo = Repo(session)
    repo.create_base_statuses()

    book = Book(title="1", author="test_author", year=2024, status_id=Statuses.AVAILABLE.value)
    repo.add_a_book(book)
    op_result = repo.remove_a_book(book.id)
    assert op_result

    found_books: list[Book] = repo.find_books()

    assert len(found_books) == 0


from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from repo.models.book import Book
from repo.models.status import Statuses, Status
from repo.repo_base import RepoBase


class Repo(RepoBase):
    _session_local: Session = ...

    def __init__(self, session_local: Session):
        self._session_local = session_local

    def create_base_statuses(self):
        for status in Statuses:
            if self._session_local.query(Status).filter_by(name=status.name).first() is None:
                self._session_local.add(Status(id=status.value, name=status.name))

        self._session_local.commit()

    def get_statuses(self) -> list[Status]:
        statuses = self._session_local.query(Status).all()
        return statuses

    def get_status_id(self, name: str) -> Optional[int]:
        status = self._session_local.query(Status).filter(Status.name == name).first()

        if status is not None:
            return status.id
        else:
            return None

    def add_a_book(self, book: Book) -> int:
        self._session_local.add(book)
        self._session_local.commit()
        return book.id

    def find_books(self, query: Optional[str] = None) -> list[Book]:
        if not query:
            return self._session_local.query(Book).all()

        search_query = f"%{query}%"
        return self._session_local.query(Book).filter(
            or_(
                Book.title.ilike(search_query),
                Book.author.ilike(search_query),
                Book.year.ilike(search_query)
            )
        ).all()

    def edit_book_status(self, book_id: int, status: Statuses) -> bool:
        book = self._session_local.query(Book).filter(Book.id == book_id).first()

        if bool is None:
            return False

        book.status_id = status.value
        self._session_local.commit()
        return True

    def remove_a_book(self, book_id: int) -> bool:
        book = self._session_local.query(Book).filter(Book.id == book_id).first()

        if bool is None:
            return False

        self._session_local.delete(book)
        self._session_local.commit()
        return True

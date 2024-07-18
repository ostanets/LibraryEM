from typing import Optional

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
            if self._session_local.query(Status).filter_by(name=status.value).first() is None:
                self._session_local.add(Status(name=status.value))

        self._session_local.commit()

    def add_a_book(self, book: Book) -> int:
        pass

    def find_books(self, query: Optional[str]) -> list[Book]:
        pass

    def edit_book_status(self, book_id: int, status: Statuses) -> bool:
        pass

    def remove_a_book(self, book_id: int) -> bool:
        pass

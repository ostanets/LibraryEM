from typing import Optional

from repo.models.book import Book
from repo.models.status import Statuses


class RepoBase:
    def create_base_statuses(self):
        raise NotImplementedError()

    def add_a_book(self, book: Book) -> int:
        raise NotImplementedError()

    def find_books(self, query: Optional[str]) -> list[Book]:
        raise NotImplementedError()

    def edit_book_status(self, book_id: int, status: Statuses) -> bool:
        raise NotImplementedError()

    def remove_a_book(self, book_id: int) -> bool:
        raise NotImplementedError()



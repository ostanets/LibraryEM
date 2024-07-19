from typing import Optional

from repo.models.book import Book
from repo.models.status import Statuses, Status


class RepoBase:
    def create_base_statuses(self):
        """
        Create base book statuses if not exists.
        """
        raise NotImplementedError()

    def get_statuses(self) -> list[Status]:
        """
        Get all book statuses.
        """
        raise NotImplementedError()

    def get_status_id(self, name: str) -> Optional[int]:
        """
        Get book status id by name.
        """
        raise NotImplementedError()

    def add_a_book(self, book: Book) -> int:
        """
        Create a new book.
        """
        raise NotImplementedError()

    def find_books(self, query: Optional[str] = None) -> list[Book]:
        """
        Find books by query.
        """
        raise NotImplementedError()

    def edit_book_status(self, book_id: int, status: Statuses) -> bool:
        """
        Edit book status by books' id.
        """
        raise NotImplementedError()

    def remove_a_book(self, book_id: int) -> bool:
        """
        Remove a book.
        """
        raise NotImplementedError()



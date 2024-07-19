import curses
from typing import List

from repo.models.book import Book
from repo.models.status import Statuses


def add_book(stdscr, repo):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "Добавление новой книги")
    stdscr.addstr(1, 0, "Название: ")
    title = stdscr.getstr(1, 10, 50).decode("utf-8")
    stdscr.addstr(2, 0, "Автор: ")
    author = stdscr.getstr(2, 7, 50).decode("utf-8")
    stdscr.addstr(3, 0, "Год выпуска: ")
    year = int(stdscr.getstr(3, 13, 4).decode("utf-8"))
    status_id = repo.get_status_id(Statuses.AVAILABLE.name)
    new_book = Book(title=title, author=author, year=year, status_id=status_id)
    book_id = repo.add_a_book(new_book)
    stdscr.addstr(5, 0, f"Добавлена новая книга с ID: {book_id}")
    stdscr.addstr(6, 0, "Нажмите любую кнопку для продолжения...")
    stdscr.getch()
    curses.noecho()


def remove_book(stdscr, repo):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "Удаление книги")
    stdscr.addstr(1, 0, "ID книги: ")
    book_id = int(stdscr.getstr(1, 10, 10).decode("utf-8"))
    success = repo.remove_a_book(book_id)
    if success:
        stdscr.addstr(3, 0, f"Книга с ID {book_id} удалена.")
    else:
        stdscr.addstr(3, 0, f"Книга с ID {book_id} не найдена.")
    stdscr.addstr(4, 0, "Нажмите любую кнопку для продолжения...")
    stdscr.getch()
    curses.noecho()


def find_book(stdscr, repo):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "Поиск книги")
    stdscr.addstr(1, 0, "Введите название, автора или год выпуска книги: ")
    query = stdscr.getstr(1, 48, 50).decode("utf-8")
    books = repo.find_books(query)
    display_books(stdscr, books)
    curses.noecho()


def list_books(stdscr, repo):
    books = repo.find_books()
    display_books(stdscr, books)


def display_books(stdscr, books: List[Book]):
    def draw_books(start_idx):
        stdscr.clear()
        if books:
            stdscr.addstr(0, 0, "ID")
            stdscr.addstr(0, 5, "Название")
            stdscr.addstr(0, 46, "Автор")
            stdscr.addstr(0, 87, "Год")
            stdscr.addstr(0, 92, "Статус")
            stdscr.addstr(1, 0, "-" * 105)
            for idx, book in enumerate(books[start_idx:start_idx + max_books_per_page], start=2):
                match book.status_id:
                    case Statuses.AVAILABLE.value:
                        status = "в наличии"
                    case Statuses.BORROWED.value:
                        status = "выдана"
                    case _:
                        status = book.status.name
                stdscr.addstr(idx, 0, f"{book.id}")
                stdscr.addstr(idx, 5, f"{(book.title[:38] + '..') if len(book.title) > 40 else book.title}")
                stdscr.addstr(idx, 46, f"{(book.author[:38] + '..') if len(book.author) > 40 else book.author}")
                stdscr.addstr(idx, 87, f"{book.year}")
                stdscr.addstr(idx, 92, f"{status}")
        else:
            stdscr.addstr(0, 0, "Не найдено ни одной книги.")
        stdscr.addstr(curses.LINES - 2, 0, "Используйте стрелки для перелистывания, 'q' для выхода.")
        stdscr.refresh()

    start_idx = 0
    max_books_per_page = curses.LINES - 4

    while True:
        draw_books(start_idx)
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_DOWN:
            if start_idx + max_books_per_page < len(books):
                start_idx += max_books_per_page
        elif key == curses.KEY_UP:
            if start_idx - max_books_per_page >= 0:
                start_idx -= max_books_per_page


def edit_book_status(stdscr, repo):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "Изменение статуса книги")
    stdscr.addstr(1, 0, "ID Книги: ")
    book_id = int(stdscr.getstr(1, 10, 10).decode("utf-8"))
    stdscr.addstr(2, 0, "Новый статус [Выберите из списка]: ")
    stdscr.addstr(3, 3, "1. В наличии")
    stdscr.addstr(4, 3, "2. Выдана")
    status_id = int(stdscr.getstr(2, 35, 1).decode("utf-8"))
    if status_id not in [1, 2]:
        stdscr.addstr(6, 0, "Статус выбран неверно. Используйте цифры 1 или 2.")
    else:
        success = repo.edit_book_status(book_id, Statuses(status_id))
        if success:
            stdscr.addstr(6, 0, f"Статус книги с ID {book_id} обновлен.")
        else:
            stdscr.addstr(6, 0, f"Книга с ID {book_id} не найдена.")
    stdscr.addstr(7, 0, "Нажмите любую кнопку для продолжения...")
    stdscr.getch()
    curses.noecho()

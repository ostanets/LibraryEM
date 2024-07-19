from repo.database import Database
from repo.repo import Repo
from ui.command_routes import *


def main(stdscr):
    curses.curs_set(0)
    Database.init_db()
    repo = Repo(Database.get_session())
    repo.create_base_statuses()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Система управления Библиотекой")
        stdscr.addstr(2, 0, "1. Добавить книгу")
        stdscr.addstr(3, 0, "2. Удалить книгу")
        stdscr.addstr(4, 0, "3. Найти книгу")
        stdscr.addstr(5, 0, "4. Каталог")
        stdscr.addstr(6, 0, "5. Изменить статус книги")
        stdscr.addstr(7, 0, "0. Выход")
        stdscr.refresh()

        choice = stdscr.getch()

        if choice == ord('1'):
            add_book(stdscr, repo)
        elif choice == ord('2'):
            remove_book(stdscr, repo)
        elif choice == ord('3'):
            find_book(stdscr, repo)
        elif choice == ord('4'):
            list_books(stdscr, repo)
        elif choice == ord('5'):
            edit_book_status(stdscr, repo)
        elif choice == ord('0'):
            break

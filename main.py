import curses

from ui.main_menu import main

if __name__ == '__main__':
    curses.wrapper(main)

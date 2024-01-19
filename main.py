import curses
import os
from main_menu import main_menu_screen


def main(screen):
    main_menu_screen(screen)

if __name__ == "__main__":
    curses.wrapper(main)
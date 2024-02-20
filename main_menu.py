import curses
import os
from writing import WritingInterface
from utils import display_manual, get_random_name, ensure_freewrites_directory
from file_manager import FileManager


def main_menu_screen(screen):
    # Menu items
    menu_items = ["<New freewrite>", "<Continue a freewrite>", "<File Manager>", "<TFW Manual>"]
    
    # Ensure the freewrites directory is created
    freewrites_directory = ensure_freewrites_directory()
    #Create an instance of the File Manager class
    file_manager = FileManager(freewrites_directory)

    current_row = 0  # Current highlighted menu item

    
    # Function to print the menu
    def print_menu(screen, selected_row):
        screen.clear()
        h, w = screen.getmaxyx()
        for idx, item in enumerate(menu_items):
            x = 0  # Start from the left edge
            y = idx  # Start from the top, and move down by idx
            if idx == selected_row:
                screen.attron(curses.color_pair(1))
                screen.addstr(y, x, item)
                screen.attroff(curses.color_pair(1))
            else:
                screen.addstr(y, x, item)
        screen.refresh()


    #Initialize color pair for selected menu item
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # White text on Black background
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Black text on white background

    #Entry point of the application
    def handle_menu_selection(screen, selection):
        if selection == 0:
            # Start a new free write
            default_filename = get_random_name()
            wi = WritingInterface(default_filename,freewrites_directory)
            wi.run(screen)
        elif selection == 1:
            #continue a previous freewrite
            file_to_continue = file_manager.select_file(screen)
            if file_to_continue:
                filepath = os.path.join(freewrites_directory, file_to_continue)
                with open(filepath, 'r') as file:
                    existing_content = file.read()
    
            #Open this file in the writing interface
            writing_interface = WritingInterface(file_to_continue, freewrites_directory, existing_content)
            writing_interface.run(screen)
        elif selection == 2:
            file_manager.show_file_management_menu(screen)
        elif selection == 3:
            display_manual(screen, 'TFW_Manual')


    # Main loop for menu navigation
    while True:
        print_menu(screen, current_row)
        key = screen.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            handle_menu_selection(screen, current_row)
        elif key == 27: # ESC key to exit
            break
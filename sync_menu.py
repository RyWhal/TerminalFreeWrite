import curses
from cloud_sync import sync_functions

def sync_menu_screen(screen):
    # Menu items
    menu_items = ["<Browse Files from anoter device>", "<More Sync Options coming>"]
    current_row = 0  # Current highlighted menu item
    sync_manager = sync_functions()

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
            pass
        elif selection == 1:
            pass       

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
        elif key == 27:
            break
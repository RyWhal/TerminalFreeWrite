import os
import curses
from pathlib import Path

class FileManager:
    def __init__(self, directory):
        self.directory = directory

    def ensure_freewrites_directory():
        freewrites_dir = os.path.join(os.getcwd(), "freewrites")
        if not os.path.exists(freewrites_dir):
            os.makedirs(freewrites_dir)
            return freewrites_dir

    def list_files(self):
        # List all .txt files with details
        pass

    def read_file(self, filename):
        # Open and display the content of the file in read-only mode
        pass

    def rename_file(self, old_filename, new_filename):
        # Rename a specified file
        pass

    def delete_file(self, filename):
        # Delete a specified file
        pass

    def cleanup_empty_files(self):
        # Find and delete all 0 size .txt files
        pass

    def show_file_management_menu(self, screen):
        
        file_menu_items = ["View free writes", "Rename free writes", "Delete free writes", "Clean-up blank free writes" ]
        current_row = 0  # Current highlighted menu item
        # Function to print the menu
        def print_menu():
            screen.clear()
            for idx, item in enumerate(file_menu_items):
                if idx == current_row:
                    screen.attron(curses.color_pair(1))
                    screen.addstr(idx, 0, item)
                    screen.attroff(curses.color_pair(1))
                else:
                    screen.addstr(idx, 0, item)
            screen.refresh()

        while True:
            print_menu()
            key = screen.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(file_menu_items) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if current_row == 0:
                    self.list_files()  # Logic to list and select files
                elif current_row == 1:
                    self.delete_file()  # Logic to delete a file
                elif current_row == 2:
                    self.cleanup_empty_files()  # Logic to cleanup empty files
                elif current_row == 3:
                    break  # Exit menu
            elif key == 27:  # ESC key
                break
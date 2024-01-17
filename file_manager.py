import os
import curses
from pathlib import Path
from datetime import datetime

class FileManager:
    def __init__(self, directory):
        self.directory = directory

    def ensure_freewrites_directory():
        freewrites_dir = os.path.join(os.getcwd(), "freewrites")
        if not os.path.exists(freewrites_dir):
            os.makedirs(freewrites_dir)
            return freewrites_dir

    def view_free_writes(self, screen):
        height, width = 25, 110  # Adjust the size as needed
        start_y, start_x = 1, 1  # Adjust the position as needed

        stats_win = curses.newwin(height, width, start_y, start_x)
        stats_win.box()

        # Now call the file_manager's list_files method
        self.list_files(stats_win) 

        stats_win.refresh()
        stats_win.getch() # Wait for key press to 

        # clear the window or screen after closing the stats window
        stats_win.clear()
        stats_win.refresh()


    def list_files(self, window):
        max_height, max_width = window.getmaxyx()
        files = [f for f in os.listdir(self.directory) if f.endswith('.txt')]
        window.clear()

        for idx, filename in enumerate(files):
            if idx < max_height - 2:  # Leave space for borders, etc.
                filepath = os.path.join(self.directory, filename)
                stats = os.stat(filepath)
                creation_date = datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d')
                modified_date = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d')
                size = stats.st_size
                word_count = self.get_word_count(filepath)

                file_info = f"{filename} | Created: {creation_date} | Modified: {modified_date} | Size: {size} bytes | Word Count: {word_count}"
                window.addstr(idx + 1, 1, file_info[:max_width-2])  # Truncate to fit the window

        window.refresh()
        window.getch()  # Wait for keypress to continue

        '''
        for filename in files:
            filepath = os.path.join(self.directory, filename)
            stats = os.stat(filepath)
            creation_date = datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            modified_date = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            size = stats.st_size
            word_count = self.get_word_count(filepath)
            print("\n")
            print(f"{filename:20} | Created: {creation_date} | Modified: {modified_date} | Size: {size} bytes | Word Count: {word_count}")
        '''

    def get_word_count(self, filepath):
        with open(filepath, 'r') as file:
            content = file.read()
            words = content.split()
            return len(words)


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
                    self.view_free_writes(screen)  # Logic to list and select files
                elif current_row == 1:
                    self.delete_file()  # Logic to delete a file
                elif current_row == 2:
                    self.cleanup_empty_files()  # Logic to cleanup empty files
                elif current_row == 3:
                    break  # Exit menu
            elif key == 27:  # ESC key
                break
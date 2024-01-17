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
        files = sorted([f for f in os.listdir(self.directory) if f.endswith('.txt')])
        window.clear()

        while True:
            key = window.getch()
            if key == 27:  # ESC key
                break
            else:
                for idx, filename in enumerate(files):
                    current_row = 0
                    if idx < max_height - 2:  # Leave space for borders, etc.
                        if idx == current_row:
                            window.attron(curses.color_pair(2))  # Use color pair 2 for highlighted text
                        else:
                            window.attron(curses.color_pair(1))  # Use color pair 1 otherwise

                        window.addstr(idx + 1, 1, filename)

                        if idx == current_row:
                            window.attroff(curses.color_pair(2))
                        else:
                            window.attroff(curses.color_pair(1))

                        window.refresh()
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

    def select_file(self, window):
        files = [f for f in os.listdir(self.directory) if f.endswith('.txt')]
        files = sorted([f for f in os.listdir(self.directory) if f.endswith('.txt')])
        current_row = 0

        def print_files():
            window.clear()
            for idx, filename in enumerate(files):
                if idx == current_row:
                    window.attron(curses.color_pair(1))  # Highlighted
                    window.addstr(idx + 1, 1, filename)
                if idx == current_row:
                    window.attroff(curses.color_pair(1))  # Normal
            window.refresh()

        while True:
            print_files()
            key = window.getch()
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(files) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return files[current_row]  # Return the selected filename

        return None

    def read_file(self, filename):
        # Open and display the content of the file in read-only mode
        pass

    def rename_file(self, old_filename, new_filename):
        # Rename a specified file
        pass

    def delete_file(self, window):
        window.clear()
        window.refresh()
        window.getch()

        filename_to_delete = self.select_file(window)
        if filename_to_delete:
            # Clear window and ask for confirmation
            window.clear()
            window.addstr(0, 0, "Are you sure you want to delete {}? (y/n): ".format(filename_to_delete))
            window.refresh()
            key = window.getch()
            if key in [ord('y'), ord('Y')]:
                os.remove(os.path.join(self.directory, filename_to_delete))
                window.addstr(1, 0, "File deleted successfully.")
                window.refresh()
                window.getch()
            else:
                window.addstr(1, 0, "Deletion cancelled.")
                window.refresh()
                window.getch()

    def cleanup_empty_files(self):
        # Find and delete all 0 size .txt files
        files = [f for f in os.listdir(self.directory) if f.endswith('.txt')]
        for filename in files:
            filepath = os.path.join(self.directory, filename)
            if os.path.getsize(filepath) == 0:
                os.remove(filepath)

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
                    break
                elif current_row == 2:
                    screen.clear()
                    self.delete_file(screen)  # Call delete_file method
                    screen.refresh()
                elif current_row == 3:
                    self.cleanup_empty_files() # Logic to cleanup empty files
            elif key == 27:  # ESC key
                break